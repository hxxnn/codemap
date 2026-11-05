const { shout } = require("./my utils.js");
const { loadItems } = require("./데이터 로더.js");

for (const item of loadItems()) {
  console.log(shout(item));
}
