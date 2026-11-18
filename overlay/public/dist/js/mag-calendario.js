/*
 * MAG — padrões dos calendários do sistema (FullCalendar 6.1.20 do Leantime 3.10.0).
 *
 * Carregado logo depois do componente de calendário (mesma ordem de "defer"), antes de
 * qualquer tela criar um calendário. Envolve FullCalendar.Calendar para que TODOS os
 * calendários (pessoal, do projeto e o widget do painel) recebam:
 *   - idioma português do Brasil ("Dia inteiro", "Hoje", "seg., ter."...);
 *   - horário comercial destacado (seg–sex, 8h–18h) e abertura rolada até 7h30;
 *   - feriados nacionais e de São Paulo, calculados aqui (sem manutenção anual);
 *   - tarefas coloridas pelo status e eventos na cor suave da marca.
 * Semana a partir de segunda e formato 24 h vêm do idioma (custom/Language/pt-BR.ini).
 */
(function () {
    'use strict';

    if (!window.FullCalendar || !FullCalendar.Calendar || !FullCalendar.globalLocales) {
        return;
    }

    // ── Configuração ─────────────────────────────────────────────────────────
    var EXPEDIENTE = { daysOfWeek: [1, 2, 3, 4, 5], startTime: '08:00', endTime: '18:00' };
    var ROLAGEM_INICIAL = '07:30:00';
    // Feriados regionais (desligar se a MAG não estiver no estado/capital de SP)
    var FERIADOS_SP_ESTADO = true;
    var FERIADOS_SP_CAPITAL = true;

    // ── Idioma português do Brasil (texto do locale oficial pt-br do FullCalendar) ──
    var ptBr = {
        code: 'pt-br',
        buttonText: {
            prev: 'Anterior', next: 'Próximo', prevYear: 'Ano anterior', nextYear: 'Próximo ano',
            today: 'Hoje', year: 'Ano', month: 'Mês', week: 'Semana', day: 'Dia', list: 'Lista'
        },
        buttonHints: {
            prev: '$0 anterior',
            next: 'Próximo $0',
            today: function (buttonText) {
                return buttonText === 'Dia' ? 'Hoje' : (buttonText === 'Semana' ? 'Esta' : 'Este') + ' ' + buttonText.toLocaleLowerCase();
            }
        },
        viewHint: function (buttonText) {
            return 'Visualizar ' + (buttonText === 'Semana' ? 'a' : 'o') + ' ' + buttonText.toLocaleLowerCase();
        },
        weekText: 'Sm',
        weekTextLong: 'Semana',
        allDayText: 'Dia inteiro',
        moreLinkText: function (n) { return 'mais +' + n; },
        moreLinkHint: function (n) { return 'Mostrar mais ' + n + ' eventos'; },
        noEventsText: 'Não há eventos para mostrar',
        navLinkHint: 'Ir para $0',
        closeHint: 'Fechar',
        timeHint: 'Hora',
        eventHint: 'Evento'
    };
    FullCalendar.globalLocales.push(ptBr);
    // O calendário pessoal chama setOption('locale', 'pt'); o código curto aponta para o mesmo texto
    FullCalendar.globalLocales.push(Object.assign({}, ptBr, { code: 'pt' }));

    function idiomaPortugues() {
        try {
            return String(leantime.i18n.__('language.code') || 'pt').toLowerCase().indexOf('pt') === 0;
        } catch (e) {
            return true;
        }
    }

    // ── Feriados ─────────────────────────────────────────────────────────────
    function pascoa(ano) { // algoritmo de Meeus/Jones/Butcher (calendário gregoriano)
        var a = ano % 19, b = Math.floor(ano / 100), c = ano % 100, d = Math.floor(b / 4), e = b % 4;
        var f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3);
        var h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4;
        var l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451);
        var mes = Math.floor((h + l - 7 * m + 114) / 31), dia = ((h + l - 7 * m + 114) % 31) + 1;
        return Date.UTC(ano, mes - 1, dia);
    }

    function iso(ms) {
        return new Date(ms).toISOString().slice(0, 10);
    }

    function diaDoAno(ano, mes, dia) {
        return iso(Date.UTC(ano, mes - 1, dia));
    }

    function feriadosDoAno(ano) {
        var p = pascoa(ano), dia = 86400000;
        var lista = [
            [diaDoAno(ano, 1, 1), 'Confraternização Universal', 'nacional'],
            [iso(p - 48 * dia), 'Carnaval (ponto facultativo)', 'facultativo'],
            [iso(p - 47 * dia), 'Carnaval (ponto facultativo)', 'facultativo'],
            [iso(p - 46 * dia), 'Quarta-feira de Cinzas (facultativo até 14h)', 'facultativo'],
            [iso(p - 2 * dia), 'Sexta-feira Santa', 'nacional'],
            [diaDoAno(ano, 4, 21), 'Tiradentes', 'nacional'],
            [diaDoAno(ano, 5, 1), 'Dia do Trabalho', 'nacional'],
            [iso(p + 60 * dia), FERIADOS_SP_CAPITAL ? 'Corpus Christi (feriado na capital SP)' : 'Corpus Christi (ponto facultativo)',
                FERIADOS_SP_CAPITAL ? 'regional' : 'facultativo'],
            [diaDoAno(ano, 9, 7), 'Independência do Brasil', 'nacional'],
            [diaDoAno(ano, 10, 12), 'Nossa Senhora Aparecida', 'nacional'],
            [diaDoAno(ano, 11, 2), 'Finados', 'nacional'],
            [diaDoAno(ano, 11, 15), 'Proclamação da República', 'nacional'],
            [diaDoAno(ano, 11, 20), 'Consciência Negra', 'nacional'],
            [diaDoAno(ano, 12, 25), 'Natal', 'nacional']
        ];
        if (FERIADOS_SP_ESTADO) {
            lista.push([diaDoAno(ano, 7, 9), 'Revolução Constitucionalista (SP)', 'regional']);
        }
        if (FERIADOS_SP_CAPITAL) {
            lista.push([diaDoAno(ano, 1, 25), 'Aniversário de São Paulo (capital)', 'regional']);
        }
        return lista;
    }

    function feriadosNoPeriodo(info, sucesso) {
        var eventos = [];
        for (var ano = info.start.getUTCFullYear(); ano <= info.end.getUTCFullYear(); ano++) {
            feriadosDoAno(ano).forEach(function (f) {
                eventos.push({
                    title: f[1], start: f[0], allDay: true,
                    classNames: ['mag-feriado', 'mag-feriado--' + f[2]]
                });
                if (f[2] !== 'facultativo') {
                    eventos.push({
                        start: f[0], allDay: true, display: 'background',
                        classNames: ['mag-feriado-fundo']
                    });
                }
            });
        }
        sucesso(eventos);
    }

    // ── Cores: tarefa pelo status, evento na cor suave da marca ──────────────
    var TEXTO_ESCURO = ['var(--grey)', 'var(--yellow)'];

    function colorirEvento(dado) {
        if (!dado || typeof dado !== 'object') {
            return dado;
        }
        if (dado.enitityType === 'ticket' && dado.borderColor) {
            // O Leantime já envia a cor do status na borda; ela passa a ser o preenchimento
            dado.backgroundColor = dado.borderColor;
            dado.textColor = TEXTO_ESCURO.indexOf(dado.borderColor) >= 0 ? '#241C1C' : '#FFFFFF';
            dado.classNames = [].concat(dado.classNames || [], 'mag-tarefa', dado.dateContext === 'due' ? 'mag-prazo' : 'mag-planejado');
        } else if (dado.enitityType === 'event') {
            dado.backgroundColor = 'var(--brand-soft)';
            dado.borderColor = 'var(--brand-solid)';
            dado.textColor = 'var(--brand-text)';
            dado.classNames = [].concat(dado.classNames || [], 'mag-evento');
        }
        return dado;
    }

    // ── Aplicação em todos os calendários ────────────────────────────────────
    function ajustar(opcoes) {
        var o = Object.assign({}, opcoes);

        if (idiomaPortugues()) {
            o.locale = 'pt-br';
        }
        if (o.businessHours === undefined) {
            o.businessHours = EXPEDIENTE;
        }
        if (o.scrollTime === undefined) {
            o.scrollTime = ROLAGEM_INICIAL;
        }
        if (o.nowIndicator === undefined) {
            o.nowIndicator = true;
        }

        var transformar = o.eventDataTransform;
        o.eventDataTransform = function (dado) {
            var resultado = transformar ? transformar(dado) : dado;
            return colorirEvento(resultado === undefined ? dado : resultado);
        };

        o.eventSources = [].concat(o.eventSources || [], [{
            id: 'mag-feriados',
            editable: false,
            events: feriadosNoPeriodo
        }]);

        return o;
    }

    var CalendarioOriginal = FullCalendar.Calendar;
    FullCalendar.Calendar = class extends CalendarioOriginal {
        constructor(elemento, opcoes) {
            super(elemento, ajustar(opcoes || {}));
        }
    };

    // Para conferência e testes
    window.magCalendario = { feriadosDoAno: feriadosDoAno, pascoa: pascoa, ajustar: ajustar };
})();
