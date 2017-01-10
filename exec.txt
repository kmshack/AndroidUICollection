#!/bin/bash

bundle exec jekyll serve
git checkout source
git add .
git commit -am 'Add new post'
git branch -D master
git checkout -b master 
git filter-branch --subdirectory-filter _site/ -f
git push --all
git checkout source