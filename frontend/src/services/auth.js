import api from './api'

export async function login(email, password) {
    const response = await api.post('/auth/login', {
    email,
    password
    })

    const { access_token, user } = response.data

    localStorage.setItem('access_token', access_token)
    localStorage.setItem('user', JSON.stringify(user))

    return user
}

export function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
}

export function getCurrentUser() {
    const user = localStorage.getItem('user')

    if (!user) {
    return null
    }

    try {
    return JSON.parse(user)
    } catch {
    logout()
    return null
    }
}

export function isAuthenticated() {
    return !!localStorage.getItem('access_token')
}