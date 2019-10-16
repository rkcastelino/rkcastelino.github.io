function resetFormPls(){
  if (document.getElementById("in radio").checked){
      var radio_val = "In"}
  else if (document.getElementById("out radio").checked){
      var radio_val = "Out"}
  document.getElementById("in/out").value = radio_val

  var job_selected = document.getElementById("job selection").value
  document.getElementById("job").value = job_selected

  const scriptURL = 'https://script.google.com/macros/s/AKfycbyLM0kKJaeoDkBudNT7bYv9DMKgHqllrfsPCWMM2llQVGZiGaT-/exec'
  const form = document.forms['submit-to-google-sheet']
  fetch(scriptURL, { method: 'POST', body: new FormData(form)})
    .then(response => console.log('Success!', response))
    .catch(error => console.error('Error!', error.message))

  alert("Clocked " + document.getElementById("in/out").value)
  document.getElementById("name").value = ""
  document.getElementById("job").value = ""
  document.getElementById("in/out").value = ""
  document.getElementById("in radio").checked = false
  document.getElementById("out radio").checked = false
  document.getElementById("job selection").value = "Laborer/Technician"
}

// Credit to  https://github.com/jamiewilson/form-to-google-sheets for the primary write to google sheet functionality!
