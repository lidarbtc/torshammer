<div align=center>
 
# Torshammer
 <p>
 <img src="https://img.shields.io/github/stars/lidarbtc/torshammer?color=%23DF0067&style=for-the-badge"/> &nbsp;
 <img src="https://img.shields.io/github/forks/lidarbtc/torshammer?color=%239999FF&style=for-the-badge"/> &nbsp;
 <img src="https://img.shields.io/github/license/lidarbtc/torshammer?color=%23E8E8E8&style=for-the-badge"/> &nbsp;
 
This is a maintained fork of Torshammer

If you want to use this with tor "browser" not "tor"

in torshammer.py change port 9050 to 9150.

## Language</br>

<img src="https://img.shields.io/badge/Python-FFDD00?style=for-the-badge&logo=python&logoColor=blue"/></br>

</div>

## Features

- user-agent spoofing
- traffic anonymize via tor
- small traffic
- works well for .onion website

## Usage on Ubuntu & Debian (python3 support)

```sh
git clone https://github.com/lidarbtc/torshammer.git

cd torshammer

pip install pysocks

sudo apt install tor

```

## Example

```sh
Use command line : python3 torshammer.py <target>
      └──────────> python3 torshammer.py example.com
```

## Limits

- It's does not work on https(443) site; only http(80).
- If server configuration is well and latest updated, it will not work.
- This is a very old proof of concept, it will not work on modern websites.

### Why?

'Cause it's slowloris tool.

I will develope get flood tool with Tor. - It should work for every website.

## Contact Developer

```sh
 lidarbtc@protonmail.com
```
