document.addEventListener('DOMContentLoaded', () => {
    const inputFile = document.getElementById('files');
    const dropzone = document.querySelector('.card');
    const fileList = document.getElementById('file-list');

    // 處理拖曳事件
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('shadow');
        dropzone.style.transform = 'scale(1.05)'; // 添加放大效果
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('shadow');
        dropzone.style.transform = 'scale(1)'; // 還原大小
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('shadow');
        dropzone.style.transform = 'scale(1)'; // 還原大小
        inputFile.files = e.dataTransfer.files;
        displayFiles();
    });

    // 處理檔案選擇事件
    inputFile.addEventListener('change', displayFiles);

    function displayFiles() {
        // 清空檔案列表
        fileList.innerHTML = '';

        // 顯示檔案名稱
        for (const file of inputFile.files) {
            const li = document.createElement('li');
            li.textContent = file.name;
            fileList.appendChild(li);
        }
    }
});