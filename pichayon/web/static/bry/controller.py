from browser import bind, ajax, document, timer


def on_complete(response):
    if response.status != 200:
        print("Failed to open door:", response.text)
        return

    data = response.json()
    document[data.get("door_id")].classList.add("disabled")
    timer.set_timeout(
        lambda: document[data.get("door_id")].classList.remove("disabled"), 5000
    )


def open_door_with_ajax(door_id):
    ajax.post(
        f"/dashboard/open_door",
        data={"door_id": door_id},
        cache=False,
        oncomplete=on_complete,
    )


@bind("div.opendoor", "click")
def open_door(ev):
    print(ev.target.id)
    door_id = ev.target.id
    open_door_with_ajax(door_id)
    print("open_door")
