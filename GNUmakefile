
.DELETE_ON_ERROR:
.SUFFIXES:

rwildcard_all = $(foreach d,$(wildcard $(addsuffix /*,$(1))),$d $(call rwildcard_all, $d))


.PHONY: all
all: maze-runner.sfc

maze-runner.sfc: wiz/bin/wiz $(call rwildcard_all, src)
	wiz/bin/wiz -I src src/main.wiz -o maze-runner.sfc


.PHONY: wiz
wiz wiz/bin/wiz:
	$(MAKE) -C wiz

wiz/bin/wiz: $(call rwildcard_all, wiz/src)


.PHONY: clean
clean:
	$(RM) maze-runner.sfc


.PHONY: clean-wiz
clean-wiz:
	$(MAKE) -C wiz clean

