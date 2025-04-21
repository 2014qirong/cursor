/**
 * image-to-pdf.js - 图片转PDF工具脚本
 */

class ImageToPdfTool {
    constructor() {
        // 配置
        this.config = {
            maxFileSize: 10 * 1024 * 1024, // 10MB
            maxFiles: 20,
            supportedTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
        };
        
        // 文件列表
        this.files = [];
        
        // DOM元素
        this.elements = {
            uploadArea: document.getElementById('uploadArea'),
            fileInput: document.getElementById('fileInput'),
            previewArea: document.getElementById('previewArea'),
            resetBtn: document.getElementById('resetBtn'),
            createPdfBtn: document.getElementById('createPdfBtn'),
            progressBar: document.getElementById('progress'),
            pageSize: document.getElementById('pageSize'),
            orientation: document.getElementById('orientation'),
            margin: document.getElementById('margin'),
            imageQuality: document.getElementById('imageQuality')
        };
        
        // 初始化
        this.init();
    }
    
    /**
     * 初始化工具
     */
    init() {
        this.setupEventListeners();
    }
    
    /**
     * 设置事件监听器
     */
    setupEventListeners() {
        const { uploadArea, fileInput, resetBtn, createPdfBtn } = this.elements;
        
        // 拖放功能
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults.bind(this), false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.highlight.bind(this), false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.unhighlight.bind(this), false);
        });
        
        uploadArea.addEventListener('drop', this.handleDrop.bind(this), false);
        
        // 文件选择
        fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        
        // 重置按钮
        resetBtn.addEventListener('click', this.resetTool.bind(this));
        
        // 生成PDF按钮
        createPdfBtn.addEventListener('click', this.createPDF.bind(this));
    }
    
    /**
     * 阻止默认事件
     */
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    /**
     * 高亮上传区域
     */
    highlight() {
        this.elements.uploadArea.classList.add('active');
    }
    
    /**
     * 取消高亮上传区域
     */
    unhighlight() {
        this.elements.uploadArea.classList.remove('active');
    }
    
    /**
     * 处理拖放文件
     */
    handleDrop(e) {
        const files = e.dataTransfer.files;
        this.processFiles(files);
    }
    
    /**
     * 处理文件选择
     */
    handleFileSelect(e) {
        const files = e.target.files;
        this.processFiles(files);
    }
    
    /**
     * 处理文件
     */
    processFiles(fileList) {
        // 验证文件数量
        if (this.files.length + fileList.length > this.config.maxFiles) {
            alert(`最多只能上传${this.config.maxFiles}张图片`);
            return;
        }
        
        // 处理每个文件
        Array.from(fileList).forEach(file => {
            // 验证文件类型
            if (!this.config.supportedTypes.includes(file.type)) {
                alert(`不支持的文件类型: ${file.type}。请上传图片文件。`);
                return;
            }
            
            // 验证文件大小
            if (file.size > this.config.maxFileSize) {
                alert(`文件 "${file.name}" 太大，超过了最大限制 ${utils.formatFileSize(this.config.maxFileSize)}`);
                return;
            }
            
            // 添加到文件列表
            this.files.push(file);
            
            // 创建预览
            this.createPreview(file);
        });
    }
    
    /**
     * 创建图片预览
     */
    createPreview(file) {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.dataset.filename = file.name;
            
            const img = document.createElement('img');
            img.src = e.target.result;
            
            const removeBtn = document.createElement('div');
            removeBtn.className = 'remove-btn';
            removeBtn.innerHTML = '<i class="fas fa-times"></i>';
            removeBtn.addEventListener('click', () => this.removeFile(file.name, previewItem));
            
            const fileName = document.createElement('div');
            fileName.className = 'file-name';
            fileName.textContent = file.name;
            
            previewItem.appendChild(img);
            previewItem.appendChild(removeBtn);
            previewItem.appendChild(fileName);
            
            this.elements.previewArea.appendChild(previewItem);
        };
        
        reader.readAsDataURL(file);
    }
    
    /**
     * 删除文件
     */
    removeFile(filename, element) {
        // 从文件列表中移除
        this.files = this.files.filter(file => file.name !== filename);
        
        // 从预览区域移除
        if (element) {
            element.remove();
        } else {
            const elements = this.elements.previewArea.querySelectorAll(`[data-filename="${filename}"]`);
            elements.forEach(el => el.remove());
        }
    }
    
    /**
     * 重置工具
     */
    resetTool() {
        this.files = [];
        this.elements.previewArea.innerHTML = '';
        this.elements.fileInput.value = '';
        this.elements.progressBar.style.width = '0';
    }
    
    /**
     * 创建PDF
     */
    async createPDF() {
        if (this.files.length === 0) {
            alert('请先上传图片');
            return;
        }
        
        // 获取配置选项
        const pageSize = this.elements.pageSize.value;
        const orientation = this.elements.orientation.value;
        const margin = parseInt(this.elements.margin.value) || 10;
        const quality = this.elements.imageQuality.value;
        
        // 质量映射
        const qualityMap = {
            'high': 1.0,
            'medium': 0.8,
            'low': 0.5
        };
        
        try {
            // 使用jsPDF库创建PDF
            // 在实际项目中，应该引入jsPDF库
            // 这里模拟生成过程
            await this.simulateConversion();
            
            // 模拟下载
            this.simulateDownload();
        } catch (error) {
            console.error('PDF生成失败:', error);
            alert('PDF生成失败，请重试');
        }
    }
    
    /**
     * 模拟转换进度
     */
    simulateConversion() {
        return new Promise((resolve) => {
            let progress = 0;
            this.elements.progressBar.style.width = '0%';
            
            const interval = setInterval(() => {
                progress += (100 / (this.files.length * 2));
                
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                    setTimeout(resolve, 500);
                }
                
                this.elements.progressBar.style.width = `${progress}%`;
            }, 200);
        });
    }
    
    /**
     * 模拟下载
     */
    simulateDownload() {
        const timestamp = new Date().toISOString().replace(/[-:.]/g, '').substring(0, 14);
        alert(`PDF生成成功！在真实应用中，这里会触发下载文件 "images_${timestamp}.pdf"。`);
    }
}

// 页面加载完成后初始化工具
document.addEventListener('DOMContentLoaded', () => {
    // 先检查是否有必要的元素
    const requiredElements = [
        'uploadArea', 'fileInput', 'previewArea', 'resetBtn', 
        'createPdfBtn', 'progress', 'pageSize', 'orientation', 
        'margin', 'imageQuality'
    ];
    
    const missing = requiredElements.filter(id => !document.getElementById(id));
    
    if (missing.length > 0) {
        console.error(`初始化失败，缺少以下元素: ${missing.join(', ')}`);
        return;
    }
    
    // 初始化工具
    window.imageToPdfTool = new ImageToPdfTool();
}); 