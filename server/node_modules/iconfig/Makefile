TESTS = $(shell ls -S `find test -type f -name "*.js" -print`)
TIMEOUT = 10000
MOCHA_OPTS =
REPORTER = tap
JSCOVERAGE = ./node_modules/jscover/bin/jscover

test:
	@NODE_ENV=test node_modules/mocha/bin/mocha \
		--reporter $(REPORTER) --timeout $(TIMEOUT) $(MOCHA_OPTS) $(TESTS)

test-cov: lib-cov
	@ICONFIG_COV=1 $(MAKE) test REPORTER=dot
	@ICONFIG_COV=1 $(MAKE) test REPORTER=html-cov > coverage.html

lib-cov:
	@rm -rf lib-cov
	@$(JSCOVERAGE) lib lib-cov

clean:
	@rm -rf lib-cov
	@rm -f coverage.html

.PHONY: lib-cov test test-cov clean