export default async function({ store, redirect }) {
	const {accessToken, refreshToken, expiresIn} = store.getters.tokens
	// console.log('MIDDLEWARE IN', accessToken, refreshToken)

	try {
		if (!refreshToken) return redirect('/login')
		const isValid = await store.dispatch('verifyAccessToken')
		if (!accessToken ||
			  expiresIn < Date.now() || 
				!isValid) {
			await store.dispatch('refreshTokens')
		}
	} catch (err) {
		console.error(err)
		return redirect('/login')
	}
}