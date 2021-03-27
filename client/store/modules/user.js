// state
export const state = () => ({
	tokens: {
		accessToken: 'startToken', //'' by default
		refreshToken: 'startToken', //'' by default
		expiresIn: Date.now() + 1800e3, //0 by default
	}
})

// getters
export const getters = ({
	tokens(state) {
		return state.tokens
	},
})

// mutations
export const mutations = ({
	updateTokens(state, tokens) {
		state.tokens = tokens
	}
})

// actions
export const actions = ({
	// Проверяет refresh токен на валидность и возвращает новую пару токенов 
	async refreshTokens(ctx) {
		const { refreshToken } = this.getters.tokens

		// Обращение к серверу
		await new Promise((res, rej) => 
			setTimeout(() => res({
				accessToken: 'refreshed',
				refreshToken: 'refreshed',
				expiresIn: Date.now() + 1800e3,
			}), 500)
		)
		.then(tokens => { 
			ctx.commit('updateTokens', tokens) 
		})		
	},
	
	// Проверяет access токен на валидность 
	async verifyAccessToken() {
		const { accessToken } = this.getters.tokens

		// Обращение к серверу
		return await new Promise((res, rej) => 
			setTimeout(() => res(true), 500)
		)
	},

	// Очистка токенов пользователя 
	async clearTokens(ctx) {
		const { accessToken } = this.getters.tokens

		// Обращение к серверу
		await new Promise((res, rej) => 
			setTimeout(() => res(), 500)
		)
		.then(() => {
			ctx.commit('updateTokens', {
				accessToken: '',
				refreshToken: '',
				expiresIn: 0,
			})
		})
	},
})

export default {
	state,
	getters,
	mutations,
	actions
}