const assert = require('assert')

browser.url('http://maxcaudle.com/climbing')

describe('climbing page mp link', () => {
    it('link to the racist should be correct', () => {
	const link = $('=The Racist')
	assert.strictEqual(link.getAttribute('href'), 'https://www.mountainproject.com/route/106001169/the-racist')
    })
})

describe('climbing page 8a link', () => {
    it('8a link should be correct', () => {
	const link  = $('=8a.nu')
	assert.strictEqual(link.getAttribute('href'), 'https://www.8a.nu/user/mason-caiby')
    })
})

