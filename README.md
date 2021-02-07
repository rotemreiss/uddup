# UDdup - URLs Deduplication Tool

The tool gets a list of URLs, and removes "duplicate" pages in the sense
of URL patterns that are probably repetitive and points to the same web template.

For example:
```
https://www.example.com/product/123
https://www.example.com/product/456
https://www.example.com/product/123?is_prod=false
https://www.example.com/product/222?is_debug=true
```
All the above are probably points to the same product "template".
Therefore it should be enough to scan only some of these URLs by our various scanners.

The result of the above after UDdup should be:
```
https://www.example.com/product/123?is_prod=false
https://www.example.com/product/222?is_debug=true
```

## Why do I need it?
Mostly for better (automated) reconnaissance process,
with less noise (for both the tester and the target).

## Examples
Take a look at `demo.txt` which is the raw URLs file which results in `demo-results.txt`.

---

## Installation
### With pip (Recommended)
```bash
pip install uddup
```

### Manual (from code)
```bash
# Clone the repository.
git clone https://github.com/rotemreiss/uddup.git

# Install the Python requirements.
cd uddup
pip install -r requirements.txt
```

---
## Usage

`uddup -u demo.txt -o ./demo-result.txt`

### More Usage Options
`uddup -h`

Short Form    | Long Form            | Description
------------- | -------------------- |-------------
-h            | --help               | Show this help message and exit
-u			  | --urls				 | File with a list of urls
-o			  | --output			 | Save results to a file
-s			  | --silent			 | Print only the result URLs
-fp           | --filter-path        | Filter paths by a given Regex

### Filter Paths by Regex
Allows filtering custom paths pattern.
For example, if we would like to filter all paths that starts with `/product` we will need to run:
```bash
# Single Regex
uddup -u demo.txt -fp "^product"
```

**Input:**
```bash
https://www.example.com/
https://www.example.com/privacy-policy
https://www.example.com/product/1
https://www.example2.com/product/2
https://www.example3.com/product/4
```

**Output:**
```bash
https://www.example.com/
https://www.example.com/privacy-policy
```

### Advanced Regex with multiple path filters
```bash
uddup -u demo.txt -fp "(^product)|(^category)"
```
---
## Contributing
Feel free to fork the repository and submit pull-requests.

---

## Support

[Create new GitHub issue][newissue]

Want to say thanks? :) Message me on <a href="https://www.linkedin.com/in/reissr" target="_blank">Linkedin</a>


---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**

<!-- Markdown helper -->
[newissue]: https://github.com/rotemreiss/uddup/issues/new
