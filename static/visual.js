document.addEventListener('DOMContentLoaded', function() {
    const width = 960;
    const height = 600;

    const svg = d3.select('body').append('svg')
        .attr('width', width)
        .attr('height', height)
        .style('border', '1px solid black');

    const tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('position', 'absolute')
        .style('background', '#fff')
        .style('padding', '10px')
        .style('border', '1px solid #999')
        .style('border-radius', '5px')
        .style('opacity', 0)
        .style('pointer-events', 'none');

    d3.json('/data').then(function(data) {
        const nodes = [
            { id: data.attore.CF, type: 'attore', ...data.attore },
            ...data.controparti.map(c => ({ id: c.CF, type: 'controparte', ...c })),
            ...data.oggetti.map(o => ({
                id: o.oggetto.descrizione,
                type: 'dirittoSoggettivo',
                ...o,
                details: o
            }))
        ];

        let links = data.oggetti.map(o => ({
            source: data.attore.CF,
            target: o.oggetto.descrizione
        }));

        // Aggiungi link da diritti soggettivi a soggetti passivi, se presenti
        data.oggetti.forEach(o => {
            if (o.natura.includes("relativo") && o.soggetti_passivi.length > 0) {
                o.soggetti_passivi.forEach(sp => {
                    if (nodes.some(n => n.id === sp.CF && (n.type === 'attore' || n.type === 'controparte'))) {
                        links.push({
                            source: o.oggetto.descrizione,
                            target: sp.CF
                        });
                    }
                });
            }
        });

        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d => d.id).distance(200))
            .force('charge', d3.forceManyBody().strength(-500))
            .force('center', d3.forceCenter(width / 2, height / 2));

        const link = svg.append('g')
            .selectAll('line')
            .data(links)
            .enter().append('line')
            .attr('stroke-width', 2)
            .attr('stroke', '#999');

        const node = svg.append('g')
            .selectAll('circle')
            .data(nodes)
            .enter().append('circle')
            .attr('r', 20)
            .attr('fill', d => {
                switch(d.type) {
                    case 'attore': return 'red';
                    case 'controparte': return 'blue';
                    default: return 'green';
                }
            })
            .on('mouseover', showTooltip)
            .on('mouseout', hideTooltip)
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));

        function showTooltip(event, d) {
            let tooltipHtml = '';
            if (d.type === 'attore' || d.type === 'controparte') {
                tooltipHtml = `CF: ${d.CF}<br>Tipo: ${d.type}`;
            } else if (d.type === 'dirittoSoggettivo') {
                tooltipHtml = `Titolo: ${d.titolo}<br>Descrizione: ${d.oggetto.descrizione}<br>Categoria: ${d.categoria.join(', ')}<br>Natura: ${d.natura.join(', ')}<br>Valore: €${d.valore}<br>Pretesa: ${d.pretesa}`;
            }
            tooltip.html(tooltipHtml)
                .style('opacity', 1)
                .style('left', `${event.pageX + 10}px`)
                .style('top', `${event.pageY - 28}px`);
        }

        function hideTooltip() {
            tooltip.style('opacity', 0);
        }

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        simulation.on('tick', () => {
            link.attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            node.attr('cx', d => Math.max(20, Math.min(width - 20, d.x)))
                .attr('cy', d => Math.max(20, Math.min(height - 20, d.y)));
        });
    }).catch(function(error) {
        console.error('Errore nel caricamento dei dati:', error);
    });
});
