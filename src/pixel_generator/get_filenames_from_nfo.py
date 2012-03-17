import codecs

nfo = codecs.open('../../sprites/bandit.nfo')

main_results = set()
for line in nfo:
    if len(line.split('.png')) > 1:
        line = 'src/' + line.partition('src/')[2]
        line = line.partition('.png')[0] + '.png'
        main_results.add(line)

deps_main = codecs.open('deps_main.txt','w','ascii')
deps_main.write('\n'.join(main_results))
deps_main.close()

generated_results = set()
for result in main_results:
    if len(result.split('output/')) > 1:
        png = result.partition('output/')[2]
        generated_results.add(png)

deps_generated = codecs.open('deps_generated.txt','w','ascii')
deps_generated.write('\n'.join(generated_results))
deps_generated.close()

cargo_results = set()
for result in generated_results:
    if len(result.split('cargo_')) > 1:
        cargo_results.add(result)

deps_cargo = codecs.open('deps_cargo.txt','w','ascii')
deps_cargo.write('\n'.join(cargo_results))
deps_cargo.close()
