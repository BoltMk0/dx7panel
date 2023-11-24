export function showMessage(message='An error occored', title='Error'){
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.top = '50%';
    container.style.left = '50%';
    container.style.transform = 'translate(-50%, -50%)';
    container.style.backgroundColor = '#633';
    container.style.padding = '5px 20px 10px 20px';
    container.style.width = '300px';
    container.style.zIndex = 999;
    container.style.boxShadow = '0 0 30px black';

    const header = document.createElement('div');
    header.style.textAlign = 'center';
    header.style.fontSize = 'larger';
    header.style.marginBottom = '10px';
    header.innerText = title;

    const body = document.createElement('div');
    body.innerText = message;
    body.style.marginBottom = '5px';

    const dismissBtn = document.createElement('button');
    dismissBtn.innerText = 'OK';
    dismissBtn.onclick = ()=>{
        document.body.removeChild(container);
    }
    dismissBtn.style.width = '100%';

    container.appendChild(header);
    container.appendChild(body);
    container.appendChild(dismissBtn);
    document.body.appendChild(container);
}