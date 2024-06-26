const id_tag = document.querySelector("#ID");
const number_tag = document.querySelector("#Number");
const interval_tag = document.querySelector("#Interval");
const button = document.querySelector("#Button");
const message_tag = document.querySelector("#Message");

let count = 0;
let event = null;

button.addEventListener("click", () =>{
    toggle();
    count = number_tag.value;
    const ids = id_tag.value

    event = setInterval(() => {
        const i = Math.floor(Math.random() * ids)
        send(i, count)
        count--;
        if (count === 0) {
            clearInterval(event);
            toggle();
        }
    }, interval_tag.value)

})

function toggle()
{
    button.disabled = !button.disabled;
}

function send(id, num)
{
    fetch("/request", {
        method: 'POST',
        redirect: 'follow',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "number": num,
            "id": id,
        })
    })
        .then(res => res.text())
        .then(data => {
            const div = document.createElement("div");
            div.innerHTML = `ID: ${id} : ${num} -- ${data}`
            message_tag.appendChild(div)
        })
}