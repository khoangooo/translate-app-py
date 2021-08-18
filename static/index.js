const translations_arr = document.getElementById("table")
const newArr = JSON.parse(translations_arr.dataset.table);

async function postData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

for (let i in newArr) {
  const myForm = document.getElementById(`form_${i}`);
  myForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const tcell = document.getElementById(`original_text_${i}`);
    const tcelId = document.getElementById(`id_${newArr[i].id}`);
    const formItem = {};
    formItem.id = tcelId.innerText;
    formItem.original_text = tcell.innerText;
    formItem.translated_text =
      myForm.elements[`tranlstated_text_modified_${i}`].value;
    const res = await postData("/", formItem);
    alert(res.msg);
  });
}

const upperLimit = document.getElementById("upper_limit");
const lowerLimit = document.getElementById("lower_limit");
const btnUpperLimit = document.getElementById("btn_upper_limit");
const btnLowerLimit = document.getElementById("btn_upper_limit");
btnUpperLimit.addEventListener("click", async function (e) {});
