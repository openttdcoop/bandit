import codecs

nfo = codecs.open('sprites/bandit.nfo')

main_results = []
for line in nfo:
    if len(line.split('.png')) > 1:
        line = 'src/' + line.partition('src/')[2]
        line = line.partition('.png')[0] + '.png'
        main_results.append(line)

deps_main = codecs.open('deps_main.txt','w','ascii')
deps_main.write('\n'.join(main_results))
deps_main.close()

graphics_results = []
for result in main_results:
    if len(result.split('cargo')) > 1:
        print 'cargo'

deps_graphics = codecs.open('deps_graphics.txt','w','ascii')
deps_graphics.write('\n'.join(graphics_results))
deps_graphics.close()
