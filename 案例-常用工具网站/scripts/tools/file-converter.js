/**
 * 文件转换器 JavaScript
 * 实现文件上传、预览和转换下载功能
 */

// 当DOM完全加载后执行初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有格式选项卡
    initFormatTabs();
    
    // 初始化所有上传区域
    initUploadAreas();
    
    // 初始化按钮事件
    initButtons();
});

// 初始化格式选项卡
function initFormatTabs() {
    const formatTabs = document.querySelectorAll('.format-tab');
    const formatContents = document.querySelectorAll('.format-content');
    
    formatTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // 移除所有活动状态
            formatTabs.forEach(t => t.classList.remove('active'));
            formatContents.forEach(c => c.classList.remove('active'));
            
            // 添加当前选项卡的活动状态
            this.classList.add('active');
            
            // 显示对应的内容
            const format = this.getAttribute('data-format');
            document.getElementById(`${format}Content`).classList.add('active');
            
            // 清空预览区域
            document.getElementById('previewArea').innerHTML = '';
        });
    });
}

// 初始化所有上传区域
function initUploadAreas() {
    // 定义所有上传区域和对应的输入框
    const uploadAreas = [
        { area: 'documentUploadArea', input: 'documentInput' },
        { area: 'imageUploadArea', input: 'imageInput' },
        { area: 'audioUploadArea', input: 'audioInput' },
        { area: 'videoUploadArea', input: 'videoInput' }
    ];
    
    // 设置每个上传区域的事件监听器
    uploadAreas.forEach(item => {
        const uploadArea = document.getElementById(item.area);
        const fileInput = document.getElementById(item.input);
        
        if (uploadArea && fileInput) {
            // 拖拽事件
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, preventDefaults, false);
            });
            
            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            // 拖拽进入和悬停
            ['dragenter', 'dragover'].forEach(eventName => {
                uploadArea.addEventListener(eventName, function() {
                    uploadArea.classList.add('active');
                });
            });
            
            // 拖拽离开和放下
            ['dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, function() {
                    uploadArea.classList.remove('active');
                });
            });
            
            // 处理拖放文件
            uploadArea.addEventListener('drop', function(e) {
                const files = e.dataTransfer.files;
                handleFiles(files, item.area.replace('UploadArea', ''));
            });
            
            // 点击上传区域触发文件选择
            uploadArea.addEventListener('click', function() {
                fileInput.click();
            });
            
            // 文件选择变化
            fileInput.addEventListener('change', function() {
                handleFiles(this.files, item.area.replace('UploadArea', ''));
            });
        }
    });
}

// 初始化按钮事件
function initButtons() {
    const convertBtn = document.getElementById('convertBtn');
    const resetBtn = document.getElementById('resetBtn');
    
    if (convertBtn) {
        convertBtn.addEventListener('click', function() {
            convertFiles();
        });
    }
    
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            resetTool();
        });
    }
}

// 处理上传的文件
function handleFiles(files, type) {
    if (!files || files.length === 0) return;
    
    // 清空预览区域
    const previewArea = document.getElementById('previewArea');
    previewArea.innerHTML = '';
    
    // 存储当前文件信息
    window.currentFiles = Array.from(files);
    window.currentFileType = type;
    
    // 为每个文件创建预览
    Array.from(files).forEach((file, index) => {
        // 检查文件大小限制
        const sizeLimit = getFileSizeLimit(type);
        if (file.size > sizeLimit) {
            showMessage(`文件 "${file.name}" 超过了大小限制：${formatFileSize(sizeLimit)}`, 'error');
            return;
        }
        
        // 创建文件预览项
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        // 选择适当的图标
        let iconClass = 'fa-file';
        if (file.type.startsWith('image/')) {
            iconClass = 'fa-file-image';
        } else if (file.type.startsWith('audio/')) {
            iconClass = 'fa-file-audio';
        } else if (file.type.startsWith('video/')) {
            iconClass = 'fa-file-video';
        } else if (file.type.includes('pdf')) {
            iconClass = 'fa-file-pdf';
        } else if (file.type.includes('word') || file.type.includes('document')) {
            iconClass = 'fa-file-word';
        } else if (file.type.includes('excel') || file.type.includes('spreadsheet')) {
            iconClass = 'fa-file-excel';
        } else if (file.type.includes('powerpoint') || file.type.includes('presentation')) {
            iconClass = 'fa-file-powerpoint';
        }
        
        // 创建预览HTML
        fileItem.innerHTML = `
            <div class="file-icon">
                <i class="fas ${iconClass}"></i>
            </div>
            <div class="file-info">
                <div class="file-name">${file.name}</div>
                <div class="file-size">${formatFileSize(file.size)}</div>
            </div>
            <div class="file-actions">
                <button class="btn btn-sm btn-outline-danger remove-file" data-index="${index}">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // 添加文件预览
        previewArea.appendChild(fileItem);
        
        // 添加删除按钮事件
        const removeBtn = fileItem.querySelector('.remove-file');
        removeBtn.addEventListener('click', function() {
            const idx = parseInt(this.getAttribute('data-index'));
            removeFile(idx);
        });
        
        // 如果是图片，添加图片预览
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '40px';
                img.style.height = '40px';
                img.style.objectFit = 'cover';
                img.style.borderRadius = '4px';
                img.style.marginRight = '10px';
                
                // 添加图片预览到文件项
                const fileIcon = fileItem.querySelector('.file-icon');
                fileIcon.innerHTML = '';
                fileIcon.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });
    
    // 显示转换选项
    showMessage('文件已添加，请选择转换选项并点击"开始转换"按钮', 'info');
}

// 删除文件
function removeFile(index) {
    if (!window.currentFiles) return;
    
    // 从数组中移除文件
    window.currentFiles.splice(index, 1);
    
    // 重新渲染预览
    const previewArea = document.getElementById('previewArea');
    previewArea.innerHTML = '';
    
    // 如果没有文件了，清空状态
    if (window.currentFiles.length === 0) {
        resetTool();
        return;
    }
    
    // 重新处理文件
    handleFiles(window.currentFiles, window.currentFileType);
}

// 获取文件大小限制
function getFileSizeLimit(type) {
    switch (type.toLowerCase()) {
        case 'document':
            return 50 * 1024 * 1024; // 50MB
        case 'image':
            return 20 * 1024 * 1024; // 20MB
        case 'audio':
            return 100 * 1024 * 1024; // 100MB
        case 'video':
            return 500 * 1024 * 1024; // 500MB
        default:
            return 10 * 1024 * 1024; // 10MB
    }
}

// 转换文件
function convertFiles() {
    if (!window.currentFiles || window.currentFiles.length === 0) {
        showMessage('请先上传文件', 'error');
        return;
    }
    
    const fileType = window.currentFileType;
    let outputFormat, quality;
    
    // 获取转换选项
    switch (fileType) {
        case 'document':
            outputFormat = document.getElementById('documentOutputFormat').value;
            quality = document.getElementById('documentQuality').value;
            break;
        case 'image':
            outputFormat = document.getElementById('imageOutputFormat').value;
            quality = document.getElementById('imageQuality').value;
            break;
        case 'audio':
            outputFormat = document.getElementById('audioOutputFormat').value;
            quality = document.getElementById('audioBitrate').value;
            break;
        case 'video':
            outputFormat = document.getElementById('videoOutputFormat').value;
            quality = document.getElementById('videoQuality').value;
            break;
    }
    
    // 显示进度条
    updateProgress(0);
    
    // 模拟转换过程
    let progress = 0;
    const interval = setInterval(function() {
        progress += 5;
        updateProgress(progress);
        
        if (progress >= 100) {
            clearInterval(interval);
            
            // 转换完成后的操作
            setTimeout(() => {
                // 下载转换后的文件
                window.currentFiles.forEach((file, index) => {
                    // 创建新的文件名
                    const fileNameParts = file.name.split('.');
                    const extension = fileNameParts.pop();
                    const baseName = fileNameParts.join('.');
                    const newFileName = `${baseName}_converted.${outputFormat}`;
                    
                    // 模拟下载
                    simulateDownload(newFileName, fileType);
                });
                
                showMessage(`文件转换完成，已为您保存${window.currentFiles.length}个文件`, 'success');
                
                // 重置进度条
                updateProgress(0);
            }, 1000);
        }
    }, 100);
}

// 更新进度条
function updateProgress(percent) {
    const progressBar = document.getElementById('progress');
    if (progressBar) {
        progressBar.style.width = `${percent}%`;
    }
}

// 模拟下载文件
function simulateDownload(fileName, fileType) {
    const link = document.createElement('a');
    
    // 这里仅模拟下载，实际情况下应该创建并使用真实的转换后文件
    const blob = new Blob(['模拟转换后的文件内容'], { type: 'application/octet-stream' });
    
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    
    setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
    }, 100);
}

// 重置工具状态
function resetTool() {
    // 清空文件数据
    window.currentFiles = [];
    window.currentFileType = null;
    
    // 清空预览区域
    document.getElementById('previewArea').innerHTML = '';
    
    // 重置进度条
    updateProgress(0);
    
    // 重置输入框
    document.getElementById('documentInput').value = '';
    document.getElementById('imageInput').value = '';
    document.getElementById('audioInput').value = '';
    document.getElementById('videoInput').value = '';
    
    // 重置转换选项
    document.getElementById('documentOutputFormat').value = 'pdf';
    document.getElementById('documentQuality').value = 'medium';
    document.getElementById('imageOutputFormat').value = 'jpg';
    document.getElementById('imageQuality').value = '80';
    document.getElementById('audioOutputFormat').value = 'mp3';
    document.getElementById('audioBitrate').value = '192';
    document.getElementById('videoOutputFormat').value = 'mp4';
    document.getElementById('videoQuality').value = 'medium';
    document.getElementById('videoResolution').value = 'original';
    
    showMessage('已重置所有设置', 'info');
}

// 显示消息
function showMessage(message, type = 'info') {
    // 创建消息元素
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas ${getIconForType(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // 添加到页面
    document.body.appendChild(toast);
    
    // 显示动画
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    // 自动消失
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// 获取消息类型对应的图标
function getIconForType(type) {
    switch (type) {
        case 'success':
            return 'fa-check-circle';
        case 'error':
            return 'fa-exclamation-circle';
        case 'warning':
            return 'fa-exclamation-triangle';
        default:
            return 'fa-info-circle';
    }
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
} 