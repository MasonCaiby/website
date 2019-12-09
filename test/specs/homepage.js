const assert = require('assert')

browser.url('http://maxcaudle.com')

describe('maxcaudle.com homepage', () => {
    it('should have the right title', () => {
        const title = browser.getTitle()
        assert.strictEqual(title, 'Max Caudle')
    })
})

describe('navbar', () => {
    it('climbing link', () => {
    const link  = $('=Climbing')
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/climbing')
    })

    it('contact link', () => {
    const link  = $('=Contact')
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/contact')
    })

    it('controls link', () => {
    const link  = $('=Controls')
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/controls')
    })

    it('wildlife detection link', () => {
    var dropdown  = $('=Projects')
    dropdown.click()
    const link  = $("=Wildlife Detection")
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/wildlife')
    })

    it('so handler link', () => {
    const link  = $('*=SO')
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/handler')
    })

    it('picnic table link', () => {
    const link  = $('*=Picnic')
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/table')
    })

    it('this website link', () => {
    const link  = $('*=Website')
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/website')
    })

    it('auto_app link', () => {
    const link  = $('*=Auto')
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/auto_app')
    })

    it('Compare Grades link', () => {
    const link  = $('*=Compare')
	assert.strictEqual(link.getAttribute('href'), 'http://maxcaudle.com/compare_grades')
    })


})

