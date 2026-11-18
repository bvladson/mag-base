<div class="center padding-lg">

    <div class="row">
        <div class="col-md-12">

            <x-global::undrawSvg
                image="undraw_goals_re_lu76.svg"
                maxWidth="auto"
                headlineSize="var(--font-size-xxxl)"
                maxheight="auto"
                height="250px"
                headline="Metas para manter o foco"
            ></x-global::undrawSvg>
        </div>
    </div>

    <div class="row ">
        <div class="col-md-12" style="font-size:var(--font-size-l);">
            <br />
            <div id="firstLoginContent">
                <p><br />As metas dividem o projeto em partes alcançáveis, mensuráveis e acionáveis.<br />Enquanto os marcos focam na execução, as metas tratam dos indicadores que você quer atingir.<br/>
                    Cada meta deve ter um objetivo claro (o que você quer alcançar) e ser medida por um único indicador.<br /><br />
                    Depois de criar a meta, ligue marcos a ela para desdobrá-la em tarefas executáveis.<br />
                </p><br />
            </div>
            <br /><br />
            <div class="row">
                <div class="col-md-12 tw-text-center">
                    <x-global::forms.button tag="a" link="javascript:void(0)" contentRole="tertiary" onclick="leantime.helperController.closeModal()">Vou explorar sozinho</x-global::forms.button>
                    <x-global::forms.button tag="a" link="javascript:void(0)" contentRole="primary" onclick="leantime.helperController.closeModal(); leantime.helperController.startGoalTour();">{{ __("buttons.start_tour") }} <i class="fa-solid fa-arrow-right"></i></x-global::forms.button>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-md-12 tw-text-center">
                    <form hx-post="{{ BASE_URL }}/help/helperModal/dontShowAgain" hx-trigger="change" hx-swap="none">
                        <label class="tw-text-sm tw-mt-sm" >
                            <input type="hidden" name="modalId" value="goals" />
                            <input type="checkbox" id="dontShowAgain" name="hidePermanently"  style="margin-top:-2px;">
                            Não mostrar novamente
                        </label>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

