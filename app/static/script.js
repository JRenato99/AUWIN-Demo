let treeData;
let margin = { top: 20, right: 50, bottom: 20, left: 50 };
let width = 1675 - margin.right - margin.left;
let height = 20000 - margin.top - margin.bottom;
let selectedNode = null;
let selectedLink = null;
let currentNodeData = null; // Almacena los datos del nodo actual.
let modoSeleccionTrabajo = false;
let nodoTrabajoData = null;
let primeraSeleccion = true;

// Obtener los elementos del modal
const modalTecnico = document.getElementById("tecnico-modal");
const modalTrabajo = document.getElementById("trabajo-modal");
const closeBtns = document.getElementsByClassName("close");
const modalPrimera = document.getElementById("modalPrimeraSeleccion");

// Eventos para cerrar los modales
closeBtns.onclick = function () {
  modalTecnico.style.display = "none";
  modalTrabajo.style.display = "none";
  modoSeleccionTrabajo = false;
};

window.onclick = function (event) {
  if (event.target == modalTecnico) {
    modalTecnico.style.display = "none";
  }
  if (event.target == modalTrabajo) {
    modalTrabajo.style.display = "none";
    modoSeleccionTrabajo = false;
  }
};

// Cargar datos de la red y inicializar el árbol
d3.json("/api/red")
  .then(function (data) {
    treeData = data;
    initTree();
  })
  .catch(function (error) {
    console.error("Error cargando datos:", error);
  });

// Inicializar la visualización del árbol
function initTree() {
  const treemap = d3.tree().size([height, width]);
  const root = d3.hierarchy(treeData);
  treemap(root);

  const svg = d3
    .select("#chart")
    .append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .attr("align", `center`);

  // Agregar enlaces (líneas)
  const links = svg
    .selectAll(".link")
    .data(root.links())
    .enter()
    .append("path")
    .attr("class", "link")
    .attr(
      "d",
      d3
        .linkHorizontal()
        .x((d) => d.y)
        .y((d) => d.x)
    )
    .attr("data-source", (d) => d.source.data.id)
    .attr("data-target", (d) => d.target.data.id)
    .on("click", function (event, d) {
      if (modoSeleccionTrabajo) {
        seleccionarNodoTrabajo(d.target);
      } else {
        selectLink(d, this);
      }
    });

  // Agregar nodos
  const nodes = svg
    .selectAll(".node")
    .data(root.descendants())
    .enter()
    .append("g")
    .attr("class", (d) => `node ${d.data.tipo}`)
    .attr("transform", (d) => `translate(${d.y},${d.x})`)
    .on("click", function (event, d) {
      if (modoSeleccionTrabajo) {
        seleccionarNodoTrabajo(d);
      } else {
        selectNode(d, this);
      }
    });

  // Agregar círculos y etiquetas a los nodos
  nodes
    .append("circle")
    .attr("r", 6)
    .attr("data-id", (d) => d.data.id);

  nodes
    .append("text")
    .attr("dy", ".35em")
    .attr("x", (d) => (d.children ? -12 : 12))
    .attr("text-anchor", (d) => (d.children ? "end" : "start"))
    .text((d) => d.data.nombre);
}

// Seleccionar un nodo
function selectNode(d, element) {
  d3.selectAll(".node.selected").classed("selected", false);
  d3.selectAll(".link.selected").classed("selected", false);
  selectedNode = element;
  d3.select(element).classed("selected", true);
  selectChildren(d);
  currentNodeData = d.data;

  // Comentado para evitar el modal de primera selección, si es necesario, descomentar
  /*
    if (primeraSeleccion) {
      modalPrimera.style.display = "block";
      return;
    }
  */

  mostrarModalTecnico(d.data);
  enviarNodoSeleccionado(d.data);
  updateInfoPanel(d.data);

  if (d.parent) {
    const parentLink = d3.select(`path[data-target="${d.data.id}"]`);
    if (!parentLink.empty()) {
      parentLink.classed("selected", true);
    }
  }
}

// Seleccionar un enlace
function selectLink(d, element) {
  if (selectedLink) {
    d3.select(selectedLink).classed("selected", false);
  }
  selectedLink = element;
  d3.select(element).classed("selected", true);

  const targetNode = d3
    .select(`circle[data-id="${d.target.data.id}"]`)
    .node().parentNode;
  selectNode(d.target, targetNode);
  updateInfoPanel(d.target.data);
}

// Seleccionar todos los nodos hijos recursivamente
function selectChildren(d) {
  if (d.children) {
    d.children.forEach((child) => {
      const childElement = d3
        .select(`circle[data-id="${child.data.id}"]`)
        .node().parentNode;
      d3.select(childElement).classed("selected", true);
      selectChildren(child);

      const linkElement = d3.select(
        `path[data-source="${d.data.id}"][data-target="${child.data.id}"]`
      );
      if (!linkElement.empty()) {
        linkElement.classed("selected", true);
      }
    });
  }
}

// Seleccionar un nodo de trabajo
function seleccionarNodoTrabajo(d) {
  d3.selectAll(".node.trabajo").classed("trabajo", false);
  const nodeElement = d3
    .select(`circle[data-id="${d.data.id}"]`)
    .node().parentNode;
  d3.select(nodeElement).classed("trabajo", true);
  nodoTrabajoData = d.data;

  document.getElementById(
    "element-trabajo"
  ).textContent = `Nodo de trabajo: ${d.data.nombre} (${d.data.id})`;

  enviarNodoTrabajo(d.data);
  //cerrarModalTrabajo();
  generarDiagnostico();
}

// Confirmar la selección de otro nodo
function confirmarSeleccionOtroNodo(si) {
  modalPrimera.style.display = "none";
  primeraSeleccion = false;

  if (si) {
    mostrarModalTrabajo(currentNodeData);
  } else {
    mostrarModalTecnico(currentNodeData);
    enviarNodoSeleccionado(currentNodeData);
    updateInfoPanel(currentNodeData);
  }
}

// Mostrar el modal del técnico
function mostrarModalTecnico(data) {
  document.getElementById(
    "modal-element-info"
  ).textContent = `${data.nombre} (${data.id})`;
  modalTecnico.style.display = "block";
}

// Manejar la respuesta del técnico
function responderTecnico(respuesta) {
  modalTecnico.style.display = "none";
  if (currentNodeData) {
    const estadoTecnico = respuesta ? "Sí (laborando)" : "No";
    document.getElementById(
      "element-tecnico"
    ).textContent = `Técnico: ${estadoTecnico}`;
    enviarInfoTecnico(currentNodeData, respuesta);

    if (respuesta) {
      mostrarModalTrabajo();
    } else {
      generarDiagnostico();
    }
  }
}

// Mostrar el modal de selección de trabajo
function mostrarModalTrabajo() {
  const modalInfo = document.getElementById("modal-trabajo-info");
  const contadorElemento = document.createElement("div");
  let segundosRestantes = 3;

  modalInfo.textContent = `Infraestructura: ${currentNodeData.nombre} (${currentNodeData.id})`;
  contadorElemento.id = "contador-regresivo";
  contadorElemento.style.marginTop = "10px";
  contadorElemento.textContent = `Cerrando en ${segundosRestantes} segundos...`;
  modalInfo.appendChild(contadorElemento);

  modalTrabajo.style.display = "block";
  modoSeleccionTrabajo = true;

  const intervalo = setInterval(() => {
    segundosRestantes--;
    contadorElemento.textContent = `Cerrando en ${segundosRestantes} segundos...`;
    if (segundosRestantes <= 0) {
      clearInterval(intervalo);
      modalTrabajo.style.display = "none";
    }
  }, 1000);
}

// Cerrar el modal de trabajo
function cerrarModalTrabajo() {
  modalTrabajo.style.display = "none";
  modoSeleccionTrabajo = false;
}

// Cancelar la selección de trabajo
function cancelarSeleccionTrabajo() {
  cerrarModalTrabajo();
  document.getElementById("element-trabajo").textContent = "Nodo de trabajo: -";
  enviarNodoTrabajo(null);
}

// Resetear la aplicación y el backend
function resetAll() {
  d3.selectAll(".node.selected").classed("selected", false);
  d3.selectAll(".link.selected").classed("selected", false);
  d3.selectAll(".node.trabajo").classed("trabajo", false);
  selectedNode = null;
  currentNodeData = null;
  nodoTrabajoData = null;
  modoSeleccionTrabajo = false;
  updateInfoPanel(selectedNode);
  limpiarDiagnostico();
  modalTecnico.style.display = "none";
  modalTrabajo.style.display = "none";

  fetch("/api/reset", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      //console.log("Servidor reseteado:", data);
    })
    .catch((error) => {
      console.error("Error al resetear en backend:", error);
    });
}

// Enviar información del técnico al servidor
function enviarInfoTecnico(nodoData, hayTecnico) {
  const data = {
    nodo: nodoData,
    hayTecnico: hayTecnico,
    timestamp: new Date().toISOString(),
  };

  fetch("/api/info-tecnico", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      //console.log("Información de técnico enviada:", data);
    })
    .catch((error) => {
      console.error("Error al enviar información de técnico:", error);
    });
}

// Enviar información del nodo de trabajo al servidor
function enviarNodoTrabajo(nodoData) {
  const data = {
    nodo_trabajo: nodoData,
    nodo_infraestructura: currentNodeData,
    timestamp: new Date().toISOString(),
  };

  fetch("/api/nodo-trabajo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      //console.log("Nodo de trabajo enviado:", data);
    })
    .catch((error) => {
      console.error("Error al enviar nodo de trabajo:", error);
    });
}

// Enviar información del nodo seleccionado al servidor
function enviarNodoSeleccionado(data) {
  fetch("/api/nodo-seleccionado", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      //console.log("Nodo seleccionado enviado:", data);
    })
    .catch((error) => {
      console.error("Error al enviar nodo seleccionado:", error);
    });
}

// Obtener el nodo seleccionado del servidor (comentado si no es necesario)
function obtenerNodoSeleccionado() {
  fetch("/api/nodo-seleccionado")
    .then((response) => response.json())
    .then((data) => {
      //console.log("Nodo seleccionado actual:", data.nodo_seleccionado);
    })
    .catch((error) => {
      console.error("Error al obtener nodo seleccionado:", error);
    });
}

// Generar y obtener el diagnóstico
function generarDiagnostico() {
  fetch("/api/generar-diagnostico")
    .then((response) => response.json())
    .then((diagnostico) => {
      mostrarDiagnosticoEnPanel(diagnostico);
    })
    .catch((error) => {
      console.error("Error al generar el diagnóstico: ", error);
    });
}

// Actualizar el panel de información
function updateInfoPanel(data) {
  if (data) {
    document.getElementById("element-id").textContent = `ID: ${data.id}`;
    document.getElementById(
      "element-name"
    ).textContent = `Nombre: ${data.nombre}`;
    document.getElementById("element-type").textContent = `Tipo: ${data.tipo}`;
    const tecnicoInfo = document.getElementById("element-tecnico").textContent;
    const trabajoInfo = document.getElementById("element-trabajo").textContent;

    if (tecnicoInfo === "Técnico: -") {
      document.getElementById("element-tecnico").textContent = "Técnico: -";
    }
    if (trabajoInfo === "Nodo de trabajo: -") {
      document.getElementById("element-trabajo").textContent =
        "Nodo de trabajo: -";
    }
  } else {
    document.getElementById("element-id").textContent = `ID: -`;
    document.getElementById("element-name").textContent = `Nombre: -`;
    document.getElementById("element-type").textContent = `Tipo: -`;
    document.getElementById("element-tecnico").textContent = `Técnico: -`;
    document.getElementById(
      "element-trabajo"
    ).textContent = `Nodo de trabajo: -`;
  }
}

// Mostrar el diagnóstico en el panel
function mostrarDiagnosticoEnPanel(diagnostico) {
  let diagnosticoElement = document.getElementById("element-diagnostico");
  if (!diagnosticoElement) {
    diagnosticoElement = document.createElement("p");
    diagnosticoElement.id = "element-diagnostico";
    document.getElementById("info-panel").appendChild(diagnosticoElement);
  }
  diagnosticoElement.innerHTML = `<strong>Diagnóstico: </strong> ${diagnostico.mensaje}`;
  diagnosticoElement.className = "";

  switch (diagnostico.tipo) {
    case "exacto":
      diagnosticoElement.classList.add("diagnostico-exacto");
      break;
    case "padre":
      diagnosticoElement.classList.add("diagnostico-padre");
      break;
    case "hijo":
      diagnosticoElement.classList.add("diagnostico-hijo");
      break;
    case "misma_infra":
      diagnosticoElement.classList.add("diagnostico-misma-infra");
      break;
    case "sin_relacion":
      diagnosticoElement.classList.add("diagnostico-sin-relacion");
      break;
    default:
      diagnosticoElement.classList.add("diagnostico-indeterminado");
      break;
  }

  if (diagnostico.detalles) {
    let detallesElement = document.getElementById("element-detalles");
    if (!detallesElement) {
      detallesElement = document.createElement("pre");
      detallesElement.id = "element-detalles";
      document.getElementById("info-panel").appendChild(detallesElement);
    }
    detallesElement.textContent = diagnostico.detalles;
  }
}

// Limpiar el diagnóstico del panel
function limpiarDiagnostico() {
  const diagnosticoElement = document.getElementById("element-diagnostico");
  const detallesElement = document.getElementById("element-detalles");
  if (diagnosticoElement) diagnosticoElement.remove();
  if (detallesElement) detallesElement.remove();
}
