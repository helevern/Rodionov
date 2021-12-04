function matr(array) {
  document.getElementById('matrix').innerHTML = '';
  var table = document.createDocumentFragment();
  var arr = [];
  var sizeRow = 4;
  var sizeCell = 5;
  if (array != undefined) {
    sizeRow = array.length+1;
    sizeCell = array[0].length+1;
  }
  for (var i = 0; i < sizeRow; i++) {
    var tr = document.createElement('tr');
    //tr.id = i;
    arr[i] = [];
    for(var j = 0; j < sizeCell; j++) {
      if(i == 0){
        var th = document.createElement('th');
        if (j == 1)
          th.innerHTML = arr[i][j] = "1";
        else if (j != 0)
          th.innerHTML = arr[i][j] = "-x" + '<sub>'+ (j-1);
        tr.appendChild(th);
      }else{
        var td = document.createElement('td');
        if (j == 0) { td.id = "Y"}
		if (j != 0){
			if (array == undefined) {
				getInput(td);
			}else{
				getInput(td,array[i-1][j-1]);
			}
		}else {
			td.innerHTML = arr[i][j] = "0=";
		}
        td.id = j;
        td.innerHTML = arr[i][j] = getRandom();
        tr.appendChild(td);
      }
    }
    table.appendChild(tr);
  }
  document.getElementById('matrix').appendChild(table);
}

function getInput(tag,array_item){
  var input = document.createElement('input');
  input.type = "number";
  if (array_item == undefined) {
    input.value = getRandom();
  }else{
    input.value = array_item;
  }
  tag.appendChild(input);
}

function getRandom(){
   var min = -10;
   var max = 10;
   return Math.floor(Math.random()*(max-min))+min;
}

function delRow(){
  var matr = document.getElementById('matrix');
  var size = matr.getElementsByTagName('tr').length - 1;
  if (size > 1) {
    matr.deleteRow(size);
  }
}

function delCell(){
  var matr = document.getElementById('matrix');
  var sizeRow = matr.getElementsByTagName('tr').length;
  var size = matr.getElementsByTagName('th').length - 1;
  if (size > 1) {
    for (var i = 0; i < sizeRow; i++) {
      matr.rows[i].deleteCell(size);  }
  }
}

function addRow(){
  var table = document.getElementById('matrix');
  var tr = table.querySelectorAll('tr');
  var len = table.querySelectorAll('th').length;
  var row = table.insertRow(tr.length);
  for (var i = 0; i < len; i++) {
    var cell = row.insertCell(i);
    if (i == 0) { 
		cell.id = "Y"
		cell.innerHTML = "0=";
	}else
		getInput(cell);
  }
}

function addCell(){
  var table = document.getElementById('matrix');
  var tr = table.querySelectorAll('tr');
  var th_len = table.querySelectorAll('th').length;
  var len = tr.length;
  for (var i = 0; i < len; i++) {
    var newCell;
    if (i == 0) {
      newCell = document.createElement('th');
      newCell.innerHTML  = "-x" + '<sub>' + (th_len-1);
    }else{
      newCell = document.createElement('td');
      getInput(newCell);
    }
    tr[i].appendChild(newCell); 
  }
}

function tableMatrix(){
  var table = document.getElementById('matrix');
  var th = table.querySelectorAll('th');
  var tr = table.querySelectorAll('tr');
  var td = table.querySelectorAll('td');
  var sizeRow = tr.length;
  var sizeCell = th.length;
  var arr = [];
  for (var i = 0; i < sizeRow; i++) {
    arr[i] = [];
    for (var j = 0; j < sizeCell; j++) {
      var k = j+(i-1)*sizeCell;
      if (i == 0 ) {
        arr[i][j] = th[j].innerHTML;
      }else{
		    if(j == 0){
		      arr[i][j] = td[k].innerHTML;
		    }else{
          var input = td[k].querySelector('input');
		      arr[i][j] = input.value;
		    }
      }
    }
  }
  return arr;      
}

function decision(){
  document.getElementById('step').innerHTML = '';
  var div_main = document.createDocumentFragment();
  var div = document.createElement('div');

  var arr = tableMatrix();
  var rank = MatrixRank(arr);

  var h2 = document.createElement('h2');
  h2.innerHTML = "Решение:";
  div_main.appendChild(h2);

  var p = document.createElement('p');
  p.innerHTML = "Дана система уравнений ";
  div.appendChild(p);

  var table = document.createElement('table');
  table.appendChild(conversionStep(arr));
  div.appendChild(table);
  div_main.appendChild(div);
  var arr_ae = [];
  var j = 0;

  for (var i = 1; i <= rank; i++) {
    var div = document.createElement('div');
    div.id = "step_" + i;
    var p = document.createElement('p');
    j = allowEntry(arr[i], arr_ae);
    p.innerHTML = "Этап №"+i+". Разрешающий элемент: " + arr[i][j] + '<sub>' + "["+i+"]"+ "["+j+"]";
    div.appendChild(p);
    arr_ae.push(j);
    arr = JordanovaException(arr, i, j);

    var table = document.createElement('table');
    table.appendChild(conversionStep(arr));
    div.appendChild(table);
    div_main.appendChild(div);
  }

  document.getElementById('step').appendChild(div_main);
  getEguations(arr,rank);
}

function conversionStep(arr){
  var table = document.createDocumentFragment();
  //getEguations(arr);
  for (var i = 0; i < arr.length; i++) {
    var tr = document.createElement('tr');
    for(var j = 0; j < arr[i].length; j++) {
      if(i == 0){
        var th = document.createElement('th');
        th.innerHTML = arr[i][j]; 
        /*if (j == 0) {
          th.innerHTML = arr[i][j];  
        }else{
          th.innerHTML = "-" + arr[i][j];  
        }*/
        tr.appendChild(th);
      }else{
        var td = document.createElement('td');
        if (j == 0) { td.id = "Y"}
        td.innerHTML = arr[i][j];
        tr.appendChild(td);
      }
    }
    table.appendChild(tr);
  }
  return table;
}

function allowEntry(arr, arr_ae){
  var n = 0;
  for (var i = 2; i < arr.length; i++) {
    for (var j = 0; j < arr_ae.length; j++) {
      if (i == arr_ae[j]) {
        n++;
      }
    }
    if (n==0 && arr[i]!=0) {
      return i;
    }else{
      n=0;
    }
  }
}

function getEguations(arr, rank){
      document.getElementById('equations').innerHTML = '';
      var div = document.createDocumentFragment();
      var h2 = document.createElement('h2');
      h2.innerHTML = "Ответ: ";
      div.appendChild(h2);
      for (var i = 1; i <= rank; i++){
        var sum = 0;
        var ex = "";
        if (!isFinite(arr[i][0])) {
          h3 = document.createElement('h3');
          h3.innerHTML += arr[i][0];
          for(var j = 1; j < arr[i].length; j++) {
            if (isFinite(arr[0][j])) {
              sum += arr[i][j]*arr[0][j];
            }else{
              if (arr[i][j] != 0 ) {
				if (arr[i][j] > 0){
					ex += "-" + arr[i][j]+"x"+'<sub>' + (j-1);
				}else {
					ex += "+" + Math.abs(arr[i][j])+"x"+'<sub>' + (j-1);
				}
              }
            }
          }
          if (ex != "" && sum != 0) {
            h3.innerHTML += +sum.toFixed(2) + ex;
          } else if (ex == "") {
              h3.innerHTML += +sum.toFixed(2);
          } else {
              h3.innerHTML += ex ;
          }
          div.appendChild(h3);
        }
      }
      document.getElementById('equations').appendChild(div);
}

function Determinant(A){
  var N = A.length, B = [], denom = 1, exchanges = 0;
  for (var i = 0; i < N; ++i){ 
    B[i] = [];
      for (var j = 0; j < N; ++j)
       B[i][j] = A[i][j];
  }
  for (var i = 0; i < N-1; ++i){ 
    var maxN = i, maxValue = Math.abs(B[i][i]);
    for (var j = i+1; j < N; ++j){ 
      var value = Math.abs(B[j][i]);
      if (value > maxValue){ 
        maxN = j; maxValue = value; 
      }
    }
    if (maxN > i){ 
      var temp = B[i]; 
      B[i] = B[maxN]; 
      B[maxN] = temp;
      ++exchanges;
    }else { 
      if (maxValue == 0) 
        return maxValue; 
    }
    var value1 = B[i][i];
    for (var j = i+1; j < N; ++j){ 
      var value2 = B[j][i];
      B[j][i] = 0;
      for (var k = i+1; k < N; ++k) 
        B[j][k] = (B[j][k]*value1-B[i][k]*value2)/denom;
    }
    denom = value1;
  }
  if (exchanges%2) 
    return -B[N-1][N-1];
  else 
    return B[N-1][N-1];
}

function MatrixRank(A){
      var m = A.length, n = A[0].length, k = (m < n ? m : n), r = 1, rank = 0;
      while (r <= k){ 
        var B = [];
        for (var i = 0; i < r; i++) 
          B[i] = [];
        for (var a = 1; a < m-r+1; a++){ 
          for (var b = 2; b < n-r+1; b++){ 
            for (var c = 0; c < r; c++){ 
              for (var d = 0; d < r; d++) 
                B[c][d] = A[a+c][b+d]; 
            }
            if (Determinant(B) != 0) 
              rank = r;
          }
        }
        r++;
      }
      return rank;
}

function JordanovaException(arr, i_ae, j_ae){
  var allow_entry = arr[i_ae][j_ae];
  var array = [];
  for (var i = 0; i < arr.length; i++) {
      array[i] = [];
    for (var j = 0; j < arr[i].length; j++) {
      if (i == i_ae && j == j_ae) {
        array[i][j] = +(1/allow_entry).toFixed(3);
      }else if (i == i_ae && j != 0) {
        array[i][j] = +(-arr[i][j]/allow_entry).toFixed(3);
      }else if (j == j_ae && i != 0){
        array[i][j] = +(arr[i][j]/allow_entry).toFixed(3);
      }else if (i == 0) {
        if (j == j_ae) {
          array[i][j] = 0;
        }else {
          array[i][j] = arr[i][j];
        }
      }else if (j == 0 ) {
        if (i == i_ae) {
          array[i][j] = "x" + '<sub>' + (i_ae) + '</sub>'+ "= ";
        }else {
          array[i][j] = arr[i][j];
        }
      }else{
        array[i][j] = +((arr[i][j]*allow_entry - arr[i][j_ae]*arr[i_ae][j])/allow_entry).toFixed(3);
      }
    }
  }
  return array;
}
