// regex for validation
const strRegex =  /^[a-zA-Z\s]*$/; // containing only letters
const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
/* supports following number formats - (123) 456-7890, (123)456-7890, 123-456-7890, 123.456.7890, 1234567890, +31636363634, 075-63546725 */
const digitRegex = /^\d+$/;

const mainForm = document.getElementById('cv-form');
const validType = {
    TEXT: 'text',
    TEXT_EMP: 'text_emp',
    EMAIL: 'email',
    DIGIT: 'digit',
    ANY: 'any',
}

// user inputs elements
let choice = document.getElementById('typeSection').value;
let timer=   document.getElementById('start_date').textContent;
let boardtypeElem = mainForm.board_type,
    ballsizeElem = mainForm.ball_size,
    pastetypeElem= mainForm.paste_type
    pastesizeElem= mainForm.paste_size,
    reflowtempElem= mainForm.reflow_temp,
    reflowtimeElem= mainForm.reflow_time;
    display_table= mainForm.displayTable;

    

// display elements

let nameDsp = document.getElementById('fullname_dsp');
let board_list={};
let paste_list={};
let testResultType = document.getElementById('typeSection2').value;
let singlePhotoResult= null;
let dropResult= 0;
let  shearResult= 0;
let  zipResult= null;
let base64Image= null;


// first value is for the attributes and second one passes the nodelists
const fetchValues = (attrs, ...nodeLists) => {
    let elemsAttrsCount = nodeLists.length;
    let elemsDataCount = nodeLists[0].length;
    let tempDataArr = [];

    // first loop deals with the no of repeaters value
    for(let i = 0; i < elemsDataCount; i++){
        let dataObj = {}; // creating an empty object to fill the data
        // second loop fetches the data for each repeaters value or attributes 
        for(let j = 0; j < elemsAttrsCount; j++){
            // setting the key name for the object and fill it with data
            dataObj[`${attrs[j]}`] = nodeLists[j][i].value;
        }
        tempDataArr.push(dataObj);
    }

    return tempDataArr;
}




const getUserInputs = (choice) => {
  // console.log(result_answer);

  if (choice === "bga") {
      boardtypeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType.TEXT, 'board_type'));
      ballsizeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType.DIGIT, 'ball_size'));
      pastetypeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType.TEXT, 'paste_type'));
      pastesizeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType.DIGIT, 'paste_size'));
      reflowtempElem.addEventListener('keyup', (e) => validateFormData(e.target, validType.DIGIT, 'reflow_temp'));
      reflowtimeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType.DIGIT, 'reflow_time'));
      
      return {
          timer: timer,
          board_type: boardtypeElem.value,
          ballsize: ballsizeElem.value,
          pastetype: pastetypeElem.value,
          pastesize: pastesizeElem.value,
          reflow_temp: reflowtempElem.value,
          reflow_time: reflowtimeElem.value,
          board_list: board_list,
          paste_list: paste_list,
          testResultType: testResultType,
          singlePhotoResult:  base64Image || singlePhotoResult, 
          shear_result:  shearResult ,
          drop_result:  dropResult ,
          zipResult: zipResult
      }
  } else if (choice === "non_bga") {
      return {
          timer: timer
          
      }
  }
};



// this is about the table

function addRow(tableId) {
    let table = document.getElementById(tableId);
    let row = document.createElement("div");
    row.className = "compositionRow";
    row.innerHTML = `
    <select class="form-control elementName">
        <option disabled selected value> -- select an element -- </option>
        <option value="Hydrogen">Hydrogen (H)</option>
        <option value="Helium">Helium (He)</option>
        <option value="Lithium">Lithium (Li)</option>
        <option value="Beryllium">Beryllium (Be)</option>
        <option value="Boron">Boron (B)</option>
        <option value="Carbon">Carbon (C)</option>
        <option value="Nitrogen">Nitrogen (N)</option>
        <option value="Oxygen">Oxygen (O)</option>
        <option value="Fluorine">Fluorine (F)</option>
        <option value="Neon">Neon (Ne)</option>
        <option value="Sodium">Sodium (Na)</option>
        <option value="Magnesium">Magnesium (Mg)</option>
        <option value="Aluminium">Aluminium (Al)</option>
        <option value="Silicon">Silicon (Si)</option>
    </select>
    <input type="text" class="form-control percentage" placeholder="Enter Percentage">
    <button type="button" class="remove-btn" onclick="removeRow(this)">-</button>
    `;
    table.appendChild(row);
}



function removeRow(button) {
    let row = button.parentNode;
    row.parentNode.removeChild(row);
}


function showTable(parentId, tableId, list) {
    let parentElem = document.getElementById(parentId);
    let compositionRows = parentElem.getElementsByClassName('compositionRow');
    let displayTable = document.getElementById(tableId);

    for(let i=0; i<compositionRows.length; i++) {
        let elementName = compositionRows[i].getElementsByClassName('elementName')[0].value;
        let percentage = compositionRows[i].getElementsByClassName('percentage')[0].value;

        list[elementName] = percentage;

        let row = displayTable.insertRow();
        let cell1 = row.insertCell();
        let cell2 = row.insertCell();
        cell1.innerHTML = elementName;
        cell2.innerHTML = percentage;
    }
}





//  show on the frontend - change the dictionry 

// removing the invalid text 
function removeErrMsg(formElem){
  formElem.nextElementSibling.innerHTML = "";
}

// adding the invalid text
function addErrMsg(formElem, formElemName){
  formElem.nextElementSibling.innerHTML = `${formElemName} is invalid`;
}

function objectToString(obj) {
    let result = [];
    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            result.push(key + ": " + obj[key]);
        }
    }
    return result.join(', ');
}


//show on the frontend -- check the vaild input

function validateFormData(elem, elemType, elemName){
  // checking for text string and non empty string
  if(elemType == validType.TEXT){
      if(!strRegex.test(elem.value) || elem.value.trim().length == 0) addErrMsg(elem, elemName);
      else removeErrMsg(elem);
  }


  if (elemType == validType.DIGIT) {
      if (!digitRegex.test(elem.value)) addErrMsg(elem, elemName);
      else removeErrMsg(elem);
  }

  // checking for only empty
  if(elemType == validType.ANY){
      if(elem.value.trim().length == 0) addErrMsg(elem, elemName);
      else removeErrMsg(elem);
  }
}


// show on the frontend -- show the print card
const displayCV = (userData) => {
    timeDsp.innerHTML= "the creating day is" + userData.timer;
    ballDsp.innerHTML ="the board type is: "+ userData.board_type  + " the ballsize is " + userData.ballsize;
    pasteDsp.innerHTML ="the paste type is: "+ userData.pastetype  + " the pastesize is " + userData.pastesize;
    reflowDsp.innerHTML=" the reflow temp is " + userData.reflow_temp + " the reflow timw is "+ userData.reflow_time;
    projects_dsp.innerHTML = `
    <p>board composition is ${objectToString(userData.board_list)}</p>
    <p>paste composition is ${objectToString(userData.paste_list)}</p>
  `;
  

   
}

// generate CV
const generateCV = () => {
    let userData = getUserInputs(choice);
    displayCV(userData);
    console.log(userData);
}

// function previewImage(){
//     let oFReader = new FileReader();
//     oFReader.readAsDataURL(imageElem.files[0]);
//     oFReader.onload = function(ofEvent){
//         imageDsp.src = ofEvent.target.result;
//     }
// }

function combinedFunction() {
    saveCVAsImage(choice).then(() => {
        sendNameToBackend();
    }).catch(error => {
        console.error("Error in combinedFunction:", error);
    });
};


function sendNameToBackend() {
    
    let userData = getUserInputs(choice);
    fetch('/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ Data: userData })
    }).then(response => response.json())
      .then(data => {
        console.log("this is the data")
        console.log(userData);  // You can handle the response from the backend here
      });
}


function saveCVAsImage() {
  let element = document.getElementById('preview-sc');
  
  // Return the promise so that you can use .then() later
  return html2canvas(element).then(function(canvas) {
      let userData = getUserInputs(choice);

      let filename = userData['board_type'] + userData['ballsize'] + userData['pastetype'] 
                   + userData['pastesize'] + userData['reflow_temp'] + '.png';

      let base64Image = canvas.toDataURL();
      sendImageToServer(base64Image, filename);
  });
}

function sendImageToServer(base64Image, filename) {
  fetch('/save_image', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          image: base64Image,
          filename: filename  // 将文件名也发送到服务器
      })
  });
}



function testImage() {
  let element = document.getElementById('singlePhotoResult');
  
  html2canvas(element).then(function(canvas) {
      base64Image = canvas.toDataURL();
  });
}



// front end   show the hirox result
function showImage(file) {
  var reader = new FileReader();

  reader.onload = function(e) {
      document.getElementById('displayImage').src = e.target.result;
      document.getElementById('displayImage').style.display = "block";
  }

  reader.readAsDataURL(file);
  generateCV();  // Assuming generateCV function is defined somewhere
}


function test_type() {
    let selection = document.getElementById('typeSection2').value;
    testResultType = selection; // Update testResultType with the current selection

    let photoInput = document.getElementById('photoInput');
    let numberInput = document.getElementById('numberInput');
    let zipInput = document.getElementById('zipInput');
    
    if (selection === 'hirox') {
      photoInput.style.display = 'block';
      numberInput.style.display = 'none';
      zipInput.style.display = 'none';

      singlePhotoResult = document.getElementById('singlePhotoResult').files[0];
      base64Image = singlePhotoResult;
      
      if (singlePhotoResult) {
          showImage(singlePhotoResult);
      }
 

    } else if (selection === 'shear_test') {
        photoInput.style.display = 'none';
        numberInput.style.display = 'block';
        zipInput.style.display = 'none';
        console.log("this is in ");
        let shear_Result= document.getElementById('numberResult');
        if (!shear_Result) {
          
          shearResult= 0;  // default to 0 if not found
        }
        else{
          shearResult=shear_Result.value;
        }

    } else if (selection === 'drop_shock') {
        photoInput.style.display = 'none';
        numberInput.style.display = 'block';
        zipInput.style.display = 'none';
        console.log("this is the new");
        let drop_Result=  document.getElementById('numberResult');
        console.log(drop_Result);
        if (!drop_Result) {
          dropResult= 0;  // default to 0 if not found
        }else{
          dropResult=drop_Result.value;

        };
        
        
    } else if (selection === 'others') {
        photoInput.style.display = 'none';
        numberInput.style.display = 'none';
        zipInput.style.display = 'block';
        zipResult = document.getElementById('zipResult').files[0];
    }

    generateCV();
}



async function handleFileUpload() {
    let userData = getUserInputs(choice);
        
    // // Generate filename based on userData 
    // let filename = userData['board_type'] + userData['ballsize'] + userData['pastetype'] 
    //              + userData['pastesize'] + userData['reflow_temp'];

    const uploadStatus = document.getElementById('uploadStatus');
    


    const formData = new FormData();
    formData.append('userData', JSON.stringify(userData));
    console.log(userData);
    console.log(formData);

    

    uploadStatus.textContent = "Uploading...";

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            uploadStatus.textContent = "Success";
        } else {
            uploadStatus.textContent = `Failed to upload: ${response.statusText}`;
        }
    } catch (error) {
        uploadStatus.textContent = `Failed to upload: ${error}`;
    }
}




// 在printCV()函数中调用saveCVAsImage
function printCV() {
    
    window.print();
}

