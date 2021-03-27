export default async function({ store, redirect }) {
	const {accessToken, refreshToken} = store.getters.tokens
	// console.log('MIDDLEWARE OUT', accessToken, refreshToken)
	
	try {
		if (accessToken) {
			const isValid = await store.dispatch('verifyAccessToken')
			if (isValid) return redirect('/')
		}	
		else if (refreshToken) {
			await store.dispatch('refreshTokens')
			if (store.getters.tokens.accessToken) return redirect('/')
		}
	} catch (err) {
		console.error(err)
		return redirect('/login')
	}
}