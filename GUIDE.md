# Guide

```javascript
console.log("%c" + document.cookie.split(";").find(v => v.startsWith("XSRF-TOKEN")).split("=")[1], "color: green;");
```
