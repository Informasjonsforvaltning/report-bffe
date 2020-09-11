# Mock server
* The mock server is a [WireMock](http://wiremock.org/) instance running on port 8080
* Stored mock data is located in the [/mock/mappings](../mock/mappings) directory
* image: rodolpheche/wiremock

## Updating mock-data
### Stubbing
*see [wiremock documentation](http://wiremock.org/docs/stubbing/)*
### Recording
1. Start mock server
2. In browser go to http://localhost:8080/__admin/recorder
3. In the box Target URL add root url of the request you want to record
4. Press "Record"
5. Replace the target url with "localhost:8080" in your request
6. Run requests `GET <url_wit_replaced_target_url>`
7. Press "Stop" in admin recorder window

The recorded data will is saved to [/mock/mappings](../mock/mappings)

#### Example value:
For http://datasets.fellesdatakatalog.digdir.no/catalogs:
  * TargetUrl: http://datasets.fellesdatakatalog.digdir.no
  * RequestUrl: http://localhost:8080/catalogs



