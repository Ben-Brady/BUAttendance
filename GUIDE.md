# Guide

Go to [website](https://cispr.bournemouth.ac.uk/study-progress)

and paste the following code into the console

```javascript
alert("Session Token:\n" + document.cookie.split(";").map(v => v.trim()).find(v => v.startsWith("XSRF-TOKEN")).split("=")[1])
```
