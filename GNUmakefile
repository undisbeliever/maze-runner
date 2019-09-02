
.DELETE_ON_ERROR:
.SUFFIXES:
MAKEFLAGS += --no-builtin-rules

rwildcard_all = $(foreach d,$(wildcard $(addsuffix /*,$(1))),$d $(call rwildcard_all, $d))


.PHONY: all
all: maze-runner.sfc

maze-runner.sfc: wiz/bin/wiz $(call rwildcard_all, src)
	wiz/bin/wiz -I src src/main.wiz -o maze-runner.sfc


.PHONY: wiz
wiz wiz/bin/wiz:
	$(MAKE) -C wiz

wiz/bin/wiz: $(call rwildcard_all, wiz/src)


gen/mode-7-tiles.m7tiles gen/mode-7-tiles.pal: tools/png2snes.py resources/mode-7-tiles.png
	python3 tools/png2snes.py -f=mode7 -c=128 -t gen/mode-7-tiles.m7tiles -p gen/mode-7-tiles.pal resources/mode-7-tiles.png

RESOURCES += gen/mode-7-tiles.m7tiles gen/mode-7-tiles.pal


gen/snake-movement-tiles.m7tiles gen/snake-movement-tiles.pal: tools/png2snes.py resources/snake-movement-tiles.png
	python3 tools/png2snes.py -f=mode7 -c=128 -t gen/snake-movement-tiles.m7tiles -p gen/snake-movement-tiles.pal resources/snake-movement-tiles.png

RESOURCES += gen/snake-movement-tiles.m7tiles gen/snake-movement-tiles.pal


gen/mode7-perepective-hdma.wiz: tools/mode7-perspective-hdma.py
	python3 tools/mode7-perspective-hdma.py > $@

RESOURCES += gen/mode7-perepective-hdma.wiz


gen/%.m7map: resources/maps/%.tmx tools/tmx2mode7map.py
	python3 tools/tmx2mode7map.py -o $@ $<

RESOURCES += $(patsubst resources/maps/%.tmx,gen/%.m7map,$(wildcard resources/maps/*.tmx))


maze-runner.sfc: $(RESOURCES)

.PHONY: resources
resources: $(RESOURCES)

$(RESOURCES): gen/
gen/:
	mkdir gen


.PHONY: clean
clean:
	$(RM) maze-runner.sfc
	$(RM) $(RESOURCES)


.PHONY: clean-wiz
clean-wiz:
	$(MAKE) -C wiz clean

