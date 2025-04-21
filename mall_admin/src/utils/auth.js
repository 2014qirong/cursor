import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'

// 获取Token
export function getToken() {
  return Cookies.get(TokenKey)
}

// 设置Token
export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

// 移除Token
export function removeToken() {
  return Cookies.remove(TokenKey)
} 