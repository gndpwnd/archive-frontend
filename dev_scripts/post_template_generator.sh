#!/bin/bash

for i in {1..50}; do

	echo "---
title: \"\"
date: \"2022-07-01\"
description: \"jp short\"
tags: [
    \"Jordan Peterson\",
]
categories: [
    \"Psychology\"
]
type: \"post\"
---
{{< rawhtml >}}
    <video style=\"height:40vh;width:auto\" overflow=\"hidden\" controls>
        <source src=\"\" type=\"video/mp4\"> 
    </video>
{{< /rawhtml >}}
" > ${PWD}/${i}.md
done
