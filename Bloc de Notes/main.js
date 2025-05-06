document.getElementById('openFile').addEventListener('click', () => {
    document.getElementById('fileInput').click();
  });
  
  document.getElementById('fileInput').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        document.getElementById('editor').value = e.target.result;
        document.getElementById('fileName').textContent = file.name;
      };
      reader.readAsText(file);
    }
  });
  
  document.getElementById('infoButton').addEventListener('click', () => {
    alert('✅ Per guardar: Control + S\n✅ Per copiar/pegar: Control + C / Control + V\n✅ Per canviar nom: doble clic sobre el nom');
  });
  
  document.getElementById('closeButton').addEventListener('click', () => {
    if (confirm('Vols tancar l’arxiu actual? El contingut no es guardarà automàticament.')) {
      document.getElementById('editor').value = '';
      document.getElementById('fileName').textContent = 'Sense arxiu';
    }
  });
  
  function ensureTxtExtension(filename) {
    if (!filename.toLowerCase().endsWith('.txt')) {
      return filename + '.txt';
    }
    return filename;
  }
  
  function downloadFile(filename, content) {
    filename = ensureTxtExtension(filename);
    const blob = new Blob([content], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  }  
  
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 's') {
      e.preventDefault();
      const content = document.getElementById('editor').value;
      let filename = document.getElementById('fileName').textContent;
      if (filename === 'Sense arxiu') filename = 'nou_arxiu.txt';
      downloadFile(filename, content);
    }
  });
  
  const fileNameElement = document.getElementById('fileName');
  fileNameElement.addEventListener('dblclick', () => {
    const newName = prompt('Introdueix el nou nom de l’arxiu (.txt si cal):', fileNameElement.textContent);
    if (newName) {
      fileNameElement.textContent = newName;
    }
  });
  