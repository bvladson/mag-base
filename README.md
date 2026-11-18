# Base MAG (sistema de tarefas)

Base do sistema de tarefas da MAG em https://task.magmoveiscorporativos.com.br: **Leantime 3.10.0** sem nenhuma marca, loja ou serviço do Leantime, com identidade visual MAG, interface do tour em português e banco de dados em instância exclusiva. Serve de ponto de partida para a ferramenta própria da MAG.

Release ativa: `3.10.0-mag5` (tradução completa para português, ativada em 29/09/2026). As anteriores (`3.10.0` original, `3.10.0-mag1` a `mag4`) continuam na VPS para reversão.

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `overlay/` | Arquivos que substituem ou se somam à release 3.10.0, nos mesmos caminhos |
| `remover.txt` | Arquivos do Leantime apagados na release |
| `alteracoes-vs-leantime-3.10.0.patch` | Diff legível de todo PHP, Blade e INI alterado |
| `tools/gerar_stubs.py`, `trocar_textos.py`, `traduzir_tour.py`, `traduzir_ajuda.py`, `gerar_idiomas.py`, `gerar_assets.py`, `traduzir_templates.py`, `traduzir_js.py`, `traduzir_php.py` | Geram o conteúdo do `overlay/` a partir dos originais; idempotentes, rodar nesta ordem. No Windows, rodar com `PYTHONIOENCODING=utf-8` (alguns imprimem emoji) |
| `tools/traducoes/*.pt-BR.ini` | Traduções das 704 chaves de idioma que o pt-BR do Leantime não tinha; lidas pelo `gerar_idiomas.py` |
| `tools/gerar_patch.py` | Regera o `alteracoes-vs-leantime-3.10.0.patch` |
| `tools/inventario_ingles.py` | Inventário de inglês restante (chaves, templates, PHP, JS) em `tools/inventario/` |
| `tools/verificar_traducao_publica.py` | Verificação sem login da tradução servida: bundles, cache-bust e dicionário `/api/i18n` |
| `tools/listar_tour.py` | Lista os passos dos tours compilados no bundle JS |
| `tools/mag-release` | Cria e ativa releases na VPS (instalado em `/usr/local/sbin/mag-release`) |
| `tools/verificar.py` | Verificação em produção: marca Leantime, rotas removidas, tour em português, cache-bust, erros |
| `tools/previa_modos.py` | Capturas dos modos claro, escuro e sistema, e do tour, sem alterar a conta |
| `tools/verificar_calendario_publico.py` | Verifica o calendário com os arquivos da produção, sem login (calendário temporário só no navegador de teste) |
| `tools/previa/calendario*.html` | Páginas locais de teste do calendário com os bundles reais do Leantime |
| `tools/banco-dedicado-corte.sh` | Script do corte para o banco exclusivo (executado uma vez, guardado como registro) |
| `tools/verificacao-*/`, `previa-modos/` | Capturas e resultados de cada publicação |

O pacote original do Leantime fica em `Downloads\Leantime-v3.10.0.zip` (SHA256 no `IMPLANTACAO.md`), extraído em `Downloads\Leantime-v3.10.0\`. O tema MAG fica em `Downloads\Leantime-deploy-20260928\tema-mag\` e, na VPS, em `/var/www/leantime/shared/themes/mag`.

## O que foi removido ou trocado

- **Loja de apps e extensões** (menu "Apps Leantime", ícone de quebra-cabeça, instalação de plugins): controllers esvaziados, rotas em 404.
- **Novidades do Leantime** (ícone de raio, feed do blog leantime.io): controllers esvaziados, rotas em 404.
- **Ajuda externa**: base de conhecimento, GitHub, Discord, contato e versão do Leantime saíram do menu "?". Ficou só "O que é esta página?".
- **"Apoie o Leantime"**: link no menu do avatar e página de doação removidos.
- **Marca**: logo, favicon, ícones de app, "powered by Leantime" e depoimentos do login. Entram os logos oficiais do Grupo MAG (gerados de `biomie/images/logo-mag.png`) e um ícone "MAG".
- **Textos**: 45 textos em pt-BR e 45 em en-US (`custom/Language/`). Também foram trocados os textos fixos em templates e PHP: integrações, convite, importação CSV e onboarding (agora em português, sem as tarefas de Discord e documentação do Leantime).
- **Tour guiado em português**: os 38 passos dos 5 tours (Meu Trabalho, painel do projeto, Kanban, marcos e metas) e os 8 modais de ajuda que os iniciam. Corrigido o link do fim do tour do Kanban, que no original apontava "Marcos" para o próprio Kanban.
- **E-mails**: o remetente é o nome do site (`LEAN_SITENAME`), o logo é o da MAG, a cor é #A61915, e os assuntos não citam o Leantime.
- **2FA**: o emissor no app autenticador passa a ser "MAG" (vale para novas ativações).
- **Telemetria** para `telemetry.leantime.io` desligada (`LEAN_ALLOW_TELEMETRY=false` no `.env`).
- **Temas**: "Less" do Leantime virou alias oculto do tema MAG. No perfil há **Claro | Escuro | Sistema**. "Sistema" segue o modo do sistema operacional (`prefers-color-scheme`), carregando o escuro por media query.

Ficam os identificadores internos de código (namespace `Leantime\`, `window.leantime`, tabelas `zp_*`, meta `leantime-version`). São invisíveis para o usuário, e renomeá-los equivaleria a reescrever o sistema. O arquivo `LICENSE` e os avisos de copyright também continuam (ver Licença).

## Tradução para português (release `3.10.0-mag5`)

O `tools/inventario_ingles.py` varreu chaves de idioma, templates Blade, mensagens PHP e bundles JS. O que chega ao usuário foi traduzido:

- **Chaves de idioma:** as 704 que faltavam no pt-BR do Leantime (canvases de estratégia, metas, stakeholders, ideias, relatórios, configurações, entre outras). Antes delas caíam no inglês. `custom/Language/pt-BR.ini` passa a ter 754 chaves. Placeholders (`%s`, `%d`, `%1$s`) conferidos um a um.
- **Templates:** 152 textos fixos em inglês e 10 ajustes pontuais com variáveis ("Progresso:", "Marco:", "Tipo:", "tarefas"), com `tools/traduzir_templates.py`.
- **JS:** menu "/" e barra do editor (104 textos), janela de envio de arquivos Uppy (144 textos, com plurais), avisos do app (tarefa atualizada, sem prazo, gráfico de progresso, rótulos de acessibilidade) e títulos dos avisos (Erro!/Aviso!/Atenção!), com `tools/traduzir_js.py`. Todos os bundles alterados passaram no `node` sem erro de sintaxe.
- **PHP:** 20 mensagens em 10 arquivos (salvar sprint, horas, marco, exportar calendário, entre outras), com `tools/traduzir_php.py`.
- **Cache-bust:** todos os bundles do cabeçalho e o `/api/i18n` levam a data do arquivo na URL, para a versão traduzida chegar sem esperar os 7 dias de cache.
- **Removido:** `Tickets/Templates/componentTest.blade.php`, página de teste de desenvolvimento sem rota.

Ficaram em inglês, de propósito:

- os nomes dos ~1.000 emojis, que só aparecem na dica do seletor de emoji;
- as descrições de opções do KaTeX e os títulos ocultos de gráficos;
- exceções e logs de desenvolvedor, ferramentas de IA e OIDC, que não são usados;
- telas removidas ou inacessíveis (ajuda externa, plugins, novidades, layout de cadastro).

Ficam iguais nos dois idiomas "Status" e "Editor".

## Calendário (nível 1, release `3.10.0-mag4`)

`overlay/public/dist/js/mag-calendario.js` é carregado logo depois do componente de calendário (FullCalendar 6.1.20) e envolve `FullCalendar.Calendar`. Assim, **todos** os calendários (pessoal, do projeto e o widget do painel) recebem os padrões abaixo:

- **Português do Brasil:** "Dia inteiro", "Hoje", "seg., ter.", "novembro de 2026". O bundle do Leantime não trazia o idioma português, e o widget nem pedia idioma.
- **Horário comercial** seg–sex das 8h às 18h, sombreando o resto, e abertura rolada até 7h30. A grade continua de 0h a 24h para nenhum compromisso fora do horário ficar escondido.
- **Feriados calculados no navegador**, sem manutenção anual (Páscoa pelo algoritmo de Meeus):
  - nacionais;
  - pontos facultativos (Carnaval, Quarta-feira de Cinzas), com borda tracejada;
  - estaduais e da capital de SP, que podem ser desligados em `FERIADOS_SP_ESTADO` e `FERIADOS_SP_CAPITAL` no topo do arquivo.
- **Cores:** tarefas preenchidas com a cor do **status**, com uma faixa escura quando é prazo. Compromissos ficam em rosa-claro da marca com borda vermelha. Feriados usam âmbar.

Formato 24 h (`language.timeformat="H:i"`) e semana a partir de segunda (`language.firstDayOfWeek="1"`) vêm de `custom/Language/pt-BR.ini`. Eles valem para o sistema todo (datas, planilhas de horas, seletores) **para quem não escolheu outro formato no perfil**. Quem salvou 12 h em Perfil → Configurações precisa trocar lá. A aparência fica em `custom.css` (seção Calendário), com tokens `--cal-*` em light/dark.

## Design system (tema)

Os componentes usam só **papéis semânticos**, e cada modo atribui valores próprios a eles:

| Papel | Claro | Escuro |
| --- | --- | --- |
| `--bg-page` | #F7F5F4 | #121010 |
| `--bg-surface` (cards) | #FFFFFF | #1A1717 |
| `--bg-surface-secondary` (itens dentro do card) | #F2EEEC | #211C1C |
| `--bg-surface-elevated` | #FFFFFF | #292222 |
| `--bg-sidebar` / `--bg-topbar` | #2A0D0D / #240B0B | #1F0C0C / #190909 |
| `--border-subtle` / `--border-strong` | #E5DDDB / #D2C5C2 | #3B3131 / #554443 |
| `--text-primary` / `-secondary` / `-muted` | #241C1C / #6F6361 / #918583 | #F6F2F1 / #B8ACAA / #8E8280 |
| `--brand-solid` / `-hover` | #A61915 / #85110E | #D83A32 / #EC4941 |
| `--brand-text` / `-soft` | #A61915 / #FBE9E7 | #F04E45 / #3A1715 |
| `--focus-ring` | #D83A32 | #F04E45 |

- `light.css` e `dark.css` são os originais do Leantime mais um bloco com esses papéis. `custom.css` mapeia os papéis para as variáveis do Leantime e tem as regras de componentes, sem cor de tema.
- `--brand-text` existe porque o vermelho de botão fica escuro demais como texto no modo escuro (#D83A32 sobre card dá 3,9:1; #F04E45 dá 5,0:1).
- `--text-muted` claro (3,6:1 sobre branco) só é usado em placeholder e texto desabilitado.
- Status e prioridade têm as mesmas cores nos dois modos, e a prioridade usada como texto tem variações próprias de cada modo.

## Banco de dados exclusivo

O sistema usa a instância MariaDB exclusiva `mariadb@tarefas` (127.0.0.1:3307, dados em `/var/lib/mysql-tarefas`, configuração em `/etc/mysql/mariadb.conf.d/99-tarefas.cnf`), com o banco `mag_tarefas` e o usuário `mag_tarefas@127.0.0.1`. Ela não compartilha processo, dados, porta, socket nem root com a instância principal, que ficou só com BIomie e Criativo em Tela. Cliente de linha de comando: `mariadb --defaults-group-suffix=.tarefas`.

## Publicar uma nova versão da base

1. Alterar o `overlay/` (ou os scripts de `tools/` e rodá-los), rodar `php -l` nos PHP alterados e atualizar o patch (`python tools/gerar_patch.py`).
2. Empacotar e enviar: `tar -cf dist-overlay.tar -C overlay .` e enviar junto com o `remover.txt` para `/root/mag-base/<nome>/` na VPS.
3. Na VPS: `mag-release criar <nome> /root/mag-base/<nome>/overlay.tar /root/mag-base/<nome>/remover.txt`. A release é criada a partir da `3.10.0`, com os links persistentes e o tema, sem ser ativada.
4. Pré-checagem: `cd /var/www/leantime/releases/<nome> && runuser -u leantime -- php bin/leantime view:cache`.
5. `mag-release ativar <nome>` e, no PC, `python tools/verificar.py` (com login) e `python tools/verificar_traducao_publica.py depois` (sem login).

Reverter: `mag-release ativar <release anterior>`.

Alterações só de tema (CSS em `tema-mag/mag/css/`) não precisam de release: basta copiar para `/var/www/leantime/shared/themes/mag/css/`. A URL do CSS leva a data do arquivo, então os navegadores recebem a versão nova.

## Armadilhas conhecidas

- **Não apagar classes PHP do Leantime.** O classmap otimizado do Composer referencia todas elas, e um arquivo ausente vira erro 500. Esvaziar a classe (ver `gerar_stubs.py`) gera 404.
- **Cache `installation` compartilhado entre releases.** Ele guarda caminhos absolutos da release anterior (`domainEvents`, `domainRoutes`). Sem esvaziá-lo, a release nova carrega os `register.php` da antiga. O `mag-release ativar` já esvazia. O `cache:clearAll` do Leantime não basta, porque só limpa o idioma en-US.
- **`/dist/` tem cache de 7 dias no Nginx.** Arquivo alterado com o mesmo nome continua antigo nos navegadores. Use nome novo (como `dist/images/mag/`) ou cache-bust (desde a `mag5`, todos os bundles do cabeçalho usam `?v=<mtime>`).
- **Tema salvo inexistente dá 500.** Nunca remover uma pasta de tema; transformá-la em alias.
- **Modais de ajuda gravam "já visto".** `help/showOnboardingDialog` marca o modal no perfil de quem o abre, então os modais não entram na verificação automática; são conferidos no arquivo da release.
- **Duas etapas não podem editar o mesmo texto.** Cada arquivo gerado tem um único script dono, senão a reexecução quebra.

## Licença

O Leantime é AGPL-3.0, sem termos adicionais. Remover a marca é permitido. A licença exige manter o `LICENSE` e os avisos de copyright no código. Como os usuários acessam o sistema pela rede (§13 da AGPL), exige também oferecer a eles o código-fonte da versão modificada, por exemplo com um link "Código-fonte" no rodapé ou no menu de ajuda.
