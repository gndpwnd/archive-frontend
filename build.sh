#!/bin/bash

domain="www.dev00ps.com"

rm -rf docs/

hugo
echo $domain > docs/CNAME

rm -rf .hugo_build.lock