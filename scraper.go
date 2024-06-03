package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"
)


/*

    Data Mining Assignment - Group 5
     
*/


type Symbols struct {
	Symbols []string `json:"symbols"`
}

type Downloader struct {
	symbols []string
}


/*
 *  New downloader
*/
func NewDownloader(symbols []string) *Downloader {
	return &Downloader{
		symbols: symbols,
	}
}


/*
 *  Download dataset
*/
func (d *Downloader) Download(symbol string, wg *sync.WaitGroup) {
	defer wg.Done()

	unixTimestamp := getCurrentUnixTimestamp()
	endpoint := fmt.Sprintf(
		"https://query1.finance.yahoo.com/v7/finance/download/" +
		"%s?period1=1410912000&period2=%s&interval=1d&events=history&includeAdjustedClose=true",
		symbol, strconv.FormatInt(unixTimestamp, 10),
	)

	resp, err := http.Get(endpoint)
	if err != nil {
		log.Printf("[ERROR] error downloading %s: %v\n", symbol, err)
		return
	}
	defer resp.Body.Close()

	filename := fmt.Sprintf("./datasets/%s.csv", symbol)
	file, err := os.Create(filename)
	if err != nil {
		log.Printf("[ERROR] error creating file for %s: %v\n", symbol, err)
		return
	}
	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		log.Printf("[ERROR] error writing data for %s: %v\n", symbol, err)
		return
	}

	fmt.Printf("[SUCCESS] saved: %s\n", symbol)
}


/*
 *  Get current UNIX timetamp
*/
func getCurrentUnixTimestamp() int64 {
	now := time.Now().UTC()
	return now.Unix()
}


func main() {
	jsonFile, err := os.Open("./postman/symbols.json")
	if err != nil {
		log.Fatalf("[ERROR] failed to open JSON file: %v", err)
	}
	defer jsonFile.Close()

	byteValue, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatalf("[ERROR] failed to read JSON file: %v", err)
	}

	var symbols Symbols
	if err := json.Unmarshal(byteValue, &symbols); err != nil {
		log.Fatalf("[ERROR] failed to unmarshal JSON: %v", err)
	}

	var wg sync.WaitGroup
	downloader := NewDownloader(symbols.Symbols)

	for _, symbol := range symbols.Symbols {
		wg.Add(1)
		go downloader.Download(symbol, &wg)
	}

	wg.Wait()
}
