/**
 * 格式化时间
 * @param {Date | string | number} time 时间
 * @param {string} format 格式
 * @returns {string}
 */
export function formatTime(time, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!time) {
    return ''
  }
  
  const date = new Date(time)
  
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()
  
  return format
    .replace(/YYYY/g, year.toString())
    .replace(/MM/g, month.toString().padStart(2, '0'))
    .replace(/DD/g, day.toString().padStart(2, '0'))
    .replace(/HH/g, hour.toString().padStart(2, '0'))
    .replace(/mm/g, minute.toString().padStart(2, '0'))
    .replace(/ss/g, second.toString().padStart(2, '0'))
}

/**
 * 格式化金额
 * @param {number} amount 金额
 * @param {number} decimals 小数位数
 * @returns {string}
 */
export function formatCurrency(amount, decimals = 2) {
  if (amount === null || amount === undefined) {
    return '--'
  }
  
  return '¥ ' + Number(amount).toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 格式化文件大小
 * @param {number} bytes 文件大小（字节）
 * @returns {string}
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 数字千分位格式化
 * @param {number} num 数字
 * @returns {string}
 */
export function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 格式化手机号
 * @param {string} phone 手机号
 * @returns {string}
 */
export function formatPhone(phone) {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

/**
 * 距离现在的时间
 * @param {Date | string | number} time 时间
 * @returns {string}
 */
export function timeAgo(time) {
  if (!time) {
    return ''
  }
  
  const date = new Date(time)
  const now = new Date()
  
  const diff = (now.getTime() - date.getTime()) / 1000
  
  if (diff < 60) {
    return '刚刚'
  } else if (diff < 3600) {
    return Math.floor(diff / 60) + '分钟前'
  } else if (diff < 86400) {
    return Math.floor(diff / 3600) + '小时前'
  } else if (diff < 2592000) {
    return Math.floor(diff / 86400) + '天前'
  } else if (diff < 31536000) {
    return Math.floor(diff / 2592000) + '个月前'
  } else {
    return Math.floor(diff / 31536000) + '年前'
  }
} 