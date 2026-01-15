let selected = "";

function selectPart(part) {
  selected = part;
  document.getElementById("info").innerHTML = `
    <h3>${part}</h3>
    KM Atual: <input id="km"><br><br>
    <button onclick="save()">Salvar troca</button>
  `;
}

function save() {
  let km = document.getElementById("km").value;

  fetch("http://127.0.0.1:8000/update?moto=FAN125&part_name=" + selected + "&km=" + km, {
    method: "POST"
  })
  .then(r => r.json())
  .then(() => alert("Salvo com sucesso!"));
}
