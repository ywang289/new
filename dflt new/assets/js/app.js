// regex for validation
const strRegex =  /^[a-zA-Z\s]*$/; // containing only letters
const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
const phoneRegex = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
/* supports following number formats - (123) 456-7890, (123)456-7890, 123-456-7890, 123.456.7890, 1234567890, +31636363634, 075-63546725 */
const digitRegex = /^\d+$/;

const mainForm = document.getElementById('cv-form');
const validType = {
    TEXT: 'text',
    TEXT_EMP: 'text_emp',
    EMAIL: 'email',
    DIGIT: 'digit',
    PHONENO: 'phoneno',
    ANY: 'any',
}

// user inputs elements
let choice = document.getElementById('typeSection').value;
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




const getUserInputs = () => {
      
        
       
        boardtypeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType.TEXT, 'board_type'));
        ballsizeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType. DIGIT, 'ball_size'));
        pastetypeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType.TEXT, 'paste_type'));
        pastesizeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType. DIGIT, 'paste_size'));
        reflowtempElem.addEventListener('keyup', (e) => validateFormData(e.target, validType. DIGIT, 'reflow_temp'));
        reflowtimeElem.addEventListener('keyup', (e) => validateFormData(e.target, validType. DIGIT, 'reflow_time'));
        console.log(board_list);
        console.log(paste_list);
    

        return {
        board_type: boardtypeElem.value
        , ballsize: ballsizeElem.value
        ,pastetype:pastetypeElem.value,
        pastesize:pastesizeElem.value,
        reflow_temp:reflowtempElem.value,
        reflow_time:reflowtimeElem.value,
        board_list: board_list,
        paste_list: paste_list


        }

};

function validateFormData(elem, elemType, elemName){
    // checking for text string and non empty string
    if(elemType == validType.TEXT){
        if(!strRegex.test(elem.value) || elem.value.trim().length == 0) addErrMsg(elem, elemName);
        else removeErrMsg(elem);
    }

    // checking for only text string
    if(elemType == validType.TEXT_EMP){
        if(!strRegex.test(elem.value)) addErrMsg(elem, elemName);
        else removeErrMsg(elem);
    }

    // checking for email
    if(elemType == validType.EMAIL){
        if(!emailRegex.test(elem.value) || elem.value.trim().length == 0) addErrMsg(elem, elemName);
        else removeErrMsg(elem);
    }

    // checking for phone number
    if(elemType == validType.PHONENO){
        if(!phoneRegex.test(elem.value) || elem.value.trim().length == 0) addErrMsg(elem, elemName);
        else removeErrMsg(elem);
    }

    // checking for only empty
    if(elemType == validType.ANY){
        if(elem.value.trim().length == 0) addErrMsg(elem, elemName);
        else removeErrMsg(elem);
    }
}

// adding the invalid text
function addErrMsg(formElem, formElemName){
    formElem.nextElementSibling.innerHTML = `${formElemName} is invalid`;
}

function addRow() {
    let table = document.getElementById("compositionTable");
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

function removeRow(element) {
    element.parentNode.remove();
}

function showTable() {
    let compositionRows = document.getElementsByClassName('compositionRow');
    let displayTable = document.getElementById('displayTable');

    for(let i=0; i<compositionRows.length; i++) {
        let elementName = compositionRows[i].getElementsByClassName('elementName')[0].value;
        let percentage = compositionRows[i].getElementsByClassName('percentage')[0].value;
        board_list[elementName]=percentage;

        let row = displayTable.insertRow();
        let cell1 = row.insertCell();
        let cell2 = row.insertCell();
        cell1.innerHTML = elementName;
        cell2.innerHTML = percentage;
    }
}

function showTable2() {
    let compositionRows = document.getElementsByClassName('compositionRow');
    let displayTable = document.getElementById('displayTable2');

    for(let i=0; i<compositionRows.length; i++) {
        let elementName = compositionRows[i].getElementsByClassName('elementName')[0].value;
        let percentage = compositionRows[i].getElementsByClassName('percentage')[0].value;
        paste_list[elementName]= percentage;

        let row = displayTable.insertRow();
        let cell1 = row.insertCell();
        let cell2 = row.insertCell();
        cell1.innerHTML = elementName;
        cell2.innerHTML = percentage;
    }
}


// removing the invalid text 
function removeErrMsg(formElem){
    formElem.nextElementSibling.innerHTML = "";
}

// show the list data
const showListData = (listData, listContainer) => {
    listContainer.innerHTML = "";
    listData.forEach(listItem => {
        let itemElem = document.createElement('div');
        itemElem.classList.add('preview-item');
        
        for(const key in listItem){
            let subItemElem = document.createElement('span');
            subItemElem.classList.add('preview-item-val');
            subItemElem.innerHTML = `${listItem[key]}`;
            itemElem.appendChild(subItemElem);
        }

        listContainer.appendChild(itemElem);
    })
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




const displayCV = (userData) => {
   
    ballDsp.innerHTML ="the board type is: "+ userData.board_type  + " the ballsize is " + userData.ballsize;
    pasteDsp.innerHTML ="the paste type is: "+ userData.pastetype  + " the pastesize is " + userData.pastesize;
    reflowDsp.innerHTML=" the reflow temp is " + userData.reflow_temp + " the reflow timw is "+ userData.reflow_time;
    projects_dsp.innerHTML = "board composition is " + objectToString(userData.board_list) + " paste composition is " + objectToString(userData.paste_list);
    
   
    
    // showListData(userData.achievements, achievementsDsp);
    // showListData(userData.skills, skillsDsp);
    // showListData(userData.educations, educationsDsp);
    // showListData(userData.experiences, experiencesDsp);
}

// generate CV
const generateCV = () => {
    let userData = getUserInputs();
    displayCV(userData);
    console.log(userData);
}

function previewImage(){
    let oFReader = new FileReader();
    oFReader.readAsDataURL(imageElem.files[0]);
    oFReader.onload = function(ofEvent){
        imageDsp.src = ofEvent.target.result;
    }
}


function sendNameToBackend() {
    
    let userData = getUserInputs();
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

// print CV
function printCV(){
    window.print();
}