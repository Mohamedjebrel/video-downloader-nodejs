// general variables //
var youtubeLink = document.querySelector(".youTubeLink")
var pasteLink = document.querySelector("#pasteLink")
var checkUrlBtn = document.querySelector(".checkUrlBtn")
var spinner = document.querySelector(".spinner")
var selectvOption = document.querySelector("#vidOptions")
var selectaOption = document.querySelector("#audOptions")
var vidpreview = document.querySelector(".vidpreview")
var imgvid = document.querySelector(".vidpreview img")
var titlevid = document.querySelector(".vid_title")
var durationvid = document.querySelector(".vid_duration")
var viewsvid = document.querySelector(".vid_views")
var likevid = document.querySelector(".vid_like")
var dislikevid = document.querySelector(".vid_dislike")
var categoriesvid = document.querySelector(".vid_categories")
var channelvid = document.querySelector(".vid_channel")
var channel_link = document.querySelector(".channel_link")
var download_section = document.querySelector(".download_section")



// event listeners
youtubeLink.onblur = function(){
  this.style.color = "#ad9fa1"
}

youtubeLink.onfocus = function(){
  this.style.color = "black"
}


// functions //
// paste tool
pasteLink.onclick = async function paste() {
  let text = await navigator.clipboard.readText();
  youtubeLink.value = text
}

// general attribure setter
function setAttributes(el, attrs) {
  for(var key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
}

// on success response
function onSuccess(response){
  console.log(response)
  spinner.style.display = "none"
  vidpreview.style.display="flex"

  // video info
  thumbnail = response["data"]["thumbnail"]
  imgvid.setAttribute("src", thumbnail)
  Object.assign(titlevid, {href:response["data"]["webpage_url"]})
  titlevid.innerHTML = response["data"]["title"]
  durationvid.innerHTML = `<b>Duration: </b>${response["data"]["duration"]}`
  viewsvid.innerHTML =  `<b>Views: </b>${response["data"]["view_count"]}`
  categoriesvid.innerHTML =  `<b>Categories: </b>${response["data"]["categories"]}`
  Object.assign(channel_link, {href:response["data"]["channel_url"]})
  channel_link.innerHTML = response["data"]["channel"]
  likevid.innerHTML =  `<b>👍: </b>${response["data"]["like_count"]}`
  dislikevid.innerHTML =  `<b>👎: </b>${response["data"]["dislike_count"]}`

  // download options
  download_section.style.display = "flex"

  // creating the download tabs and their contents
  extensions = []
  for (var i=0; i<=response["data"]["formats"].length-1; i++){
    if (extensions.includes(response["data"]["formats"][i]["ext"])){
      pass = null
    }
    else{
      extensions.push(response["data"]["formats"][i]["ext"])
      console.log(response["data"]["formats"][i]["ext"])
    }
  }

  for (var i=1; i<=extensions.length; i++){
    document.querySelector(".holy-tabs").insertAdjacentHTML("beforeend",`
                <input class="holy-tab-input ${extensions[i-1]}" id="holy-tab-${i}" type="radio" name="choice">
                <label class="holy-tab" for="holy-tab-${i}">${extensions[i-1]}</label>
            `)
    if (i-1==0){document.querySelector("#holy-tab-1").checked = true} else {var pass}
  }

  for (var i=1; i<=extensions.length; i++){
    document.querySelector(".holy-tabs").insertAdjacentHTML("beforeend",`
            <div class="holy-content ext-${extensions[i-1]}">
              <table class="c-table">
              <thead class="c-table__header">
                <tr>
                  <th class="c-table__col-label quality">Quality</th>
                  <th class="c-table__col-label file_size">File Size</th>
                  <th class="c-table__col-label download">Download</th>
                </tr>
              </thead>
              <tbody class="c-table__body">
                
              </tbody>
            </table> 
          </div>
            `)
  }

  var tabs = document.querySelectorAll(".holy-content")
  for (var i=0; i <= tabs.length; i++){
    try {
      extvalue = tabs[i].classList[1].split('ext-')[1]
      for (var x=0; x<=response["data"]["formats"].length-1; x++){
        if(response["data"]["formats"][x]["ext"] == extvalue){
          if (response["data"]["formats"][x]["format"].includes("audio")) {var src="static/images/audio.png"} else {var src="static/images/video.png"}
          document.querySelector(`.ext-${extvalue}`).querySelector(`.c-table`).querySelector(`.c-table__body`).insertAdjacentHTML("beforeend", `
            <tr>
              <td class="c-table__cell"><img src="${src}" width="30" height="30"><span class="quality_cell">${response["data"]["formats"][x]["format"]}</span></td>
              <td class="c-table__cell">${response["data"]["formats"][x]["filesize"]}</td>
              <td class="c-table__cell"><input class="downloadBtn" type="button" value="Download" onclick="download(this)" data="${response["data"]["formats"][x]["ext"] + "," + response["data"]["formats"][x]["format"] + "," + response["data"]["formats"][x]["filesize"]}"></td>
            </tr>`)
        }
      }
    }
    finally{
      continue
    }
  }
  // modifying and handling the table // 
  var downloadtablecells = document.querySelectorAll(".quality_cell")
  for (var i=0; i<=downloadtablecells.length-1; i++){
    console.log(downloadtablecells[i])
    if (downloadtablecells[i].textContent.includes("audio")){ 
      downloadtablecells[i].textContent = "Audio"
    }
  }
  console.log("Done")
  console.log(response);
}


// sending url to the server to check //
checkUrlBtn.onclick = function(){
  spinner.style.display = "block"

  var data = {url:youtubeLink.value}
  $.ajax({
          type: "POST",
          url: "/urlchecker",
          contentType: "application/json",
          data: JSON.stringify(data),
          dataType: "json",
          success: function(response){
            onSuccess(response)},
          error: function(err) {
            spinner.style.display = "none"
              console.log(err);
          }
        });
}

// sending download request to the server and following the progress //

function download(el){
    var data = {data:$(el).attr("data")}
    // download request
    var download_response 
    $.ajax({
            type: "POST",
            url: "/download",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            success: function(response){
              console.log(response)
              setInterval(download_progress(), 500)
            },
            error: function(err) {
              spinner.style.display = "none"
              download_response = 0
              console.log(err);
            }
          });
}

function download_progress(){
  $.ajax({
    type: "GET",
    url: "/downloadProgress",
    contentType: "application/json",
    dataType: "json",
    success: function(response){
      console.log(response["status"])
      console.log(response["progress"])
    },
    error: function(err) {
        console.log(err);
    }
  });
}