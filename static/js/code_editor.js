
    let editor;
    const outputEl = document.getElementById('output');
    const csrfToken = '{{ csrf_token }}';

    // Dynamically load Monaco Editor
    const monacoLoaderScript = document.createElement('script');
    monacoLoaderScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.0/min/vs/loader.js';
    monacoLoaderScript.onload = function () {
        require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.0/min/vs' } });

    require(['vs/editor/editor.main'], function () {
        console.log("Monaco Editor Loaded");
    editor = monaco.editor.create(document.getElementById('editorContainer'), {
        value: '# Write your Python code here\n',
    language: 'python',
    theme: 'vs-dark',
    automaticLayout: true,
            });
        });
    };
    monacoLoaderScript.onerror = function () {
        console.error('Failed to load Monaco Editor');
    };
    document.head.appendChild(monacoLoaderScript);

    async function sendCode(url, formData) {
        try {
            const response = await fetch(url, {
        method: 'POST',
    body: formData,
    headers: {'X-CSRFToken': csrfToken }
            });

    if (response.ok) {
                const data = await response.json();
    if (data.status === "success") {
        alert('Correct answer');
    outputEl.textContent = `Correct answer \n\n Output\n\n ${data.output}`;
                } else if (data.status === "not allowed") {
        alert('Already answered');
    outputEl.textContent = `Already answered\n\n Output\n\n${data.output}`;
                } else if (data.status === 'error') {
        outputEl.textContent = `Error \n\n Output\n\n${data.output}`;
                } else {
        alert(data.message);
    console.log(data);
    outputEl.textContent = `Try again \n\n Output\n\n ${data.output}`;
                }
            } else {
        alert("Error: Something went wrong");
            }
        } catch (err) {
        alert('Error: Unable to connect');
        }
    }

    async function getInputd() {
        const input = editor.getValue();
    const formd = new FormData();
    formd.append('program', input);
    formd.append('qid', sessionStorage.getItem('qid'));
    formd.append('user_id', sessionStorage.getItem('user_id'));
    const url = `http://127.0.0.1:8000/checkanswerd/`;
    await sendCode(url, formd);
    }

    async function getInputw() {
        const input = editor.getValue();
    const formd = new FormData();
    formd.append('program', input);
    formd.append('qid', sessionStorage.getItem('qid'));
    formd.append('user_id', sessionStorage.getItem('user_id'));
    const url = `http://127.0.0.1:8000/checkanswerw/`;
    await sendCode(url, formd);
    }

    async function getInputc() {
        const input = editor.getValue();
    const formd = new FormData();
    formd.append('program', input);
    formd.append('qid', sessionStorage.getItem('qid'));
    formd.append('user_id', sessionStorage.getItem('user_id'));
    const url = `http://127.0.0.1:8000/checkanswerc/`;
    await sendCode(url, formd);
    }
