<div class="center padding-lg">

    <div class="row">
        <div class="col-md-12">
            <div style='width:50%' class='svgContainer'>
                {!! file_get_contents(ROOT . '/dist/images/svg/undraw_design_data_khdb.svg') !!}
            </div>
            <h1>Defina seus projetos com facilidade</h1><br />
            <p>Os modelos ajudam a organizar todas as informações. O sistema oferece ferramentas e canvases para definir o contexto do projeto, como Canvas de Modelo de Negócio, Análise SWOT ou Mapa de Empatia.<br /><br />
            Se não souber por onde começar, crie um "Canvas de Valor do Projeto". Ele responde às perguntas mais importantes do projeto:

                Quem é o seu cliente? <br />
                Que problema você está resolvendo?<br />
                Qual é a sua solução?<br />
                Que vantagem sua solução oferece em relação aos concorrentes?<br />
            </p>
            <br /><br />
        </div>
    </div>


    <div class="row">
        <div class="col-md-12">

            <x-global::forms.button tag="a" link="{{ BASE_URL }}/valuecanvas/showCanvas" contentRole="primary">Criar um Canvas de Valor do Projeto</x-global::forms.button><br />

        </div>
    </div>


</div>
