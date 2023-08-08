railcard_object = document.createElement("div")
railcard_object.setAttribute("id","railcard")
railcard_headbar = document.createElement("div")
railcard_headbar.setAttribute("id","railcard_headbar")
railcard_detail = document.createElement("div")
railcard_detail.setAttribute("id","railcard_detail")
railcard_detail_img = document.createElement("img")
railcard_detail_img.setAttribute("id", "railcard_detail_img")
railcard_detail.appendChild(railcard_detail_img)

chara_img_list = []

function showCharacter(e) {
    chara_img_list.forEach(element => {
        element_chara_rarity = element.id.split('-')[1]
        element.classList.remove("rarity" + element_chara_rarity)
    });
    chara_rarity = this.id.split('-')[1]
    this.classList.add("rarity" + chara_rarity)
    character_obj_img = document.getElementById("railcard_detail_img")
    character_obj_img.setAttribute("src", imgdir + "/card-" + this.id + ".jpg")
}

characters.forEach(character => {
    chara_div = document.createElement("div")
    chara_div.setAttribute("class", "imgdiv")
    chara_img = document.createElement("img")
    chara_img.setAttribute("id",character)
    chara_img.setAttribute("src",`${imgdir}/avatar-${character}.png`)
    chara_img.addEventListener('click', showCharacter)
    chara_img_list.push(chara_img)
    chara_div.appendChild(chara_img)
    railcard_headbar.appendChild(chara_div)
});

railcard_object.appendChild(railcard_headbar)
railcard_object.appendChild(railcard_detail)
document.getElementsByTagName("railcard")[0].replaceWith(railcard_object)
chara_img_list[0].click()
