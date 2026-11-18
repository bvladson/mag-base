
<div class="center padding-lg" style="width:800px;">
    <div class="row">
        <div class="col-md-12">
            <x-global::undrawSvg
                image="undraw_joyride_re_968t.svg"
                maxWidth="auto"
                headlineSize="var(--font-size-xxxl)"
                maxheight="auto"
                height="250px"
                headline="Gestão de projetos"
            ></x-global::undrawSvg>
        </div>
    </div>
    <div class="row onboarding">
        <div class="col-md-12" style="font-size:var(--font-size-l);">
            <br />
            <div id="firstLoginContent">
                <p><br />Projetos são espaços de trabalho colaborativos onde você e sua equipe organizam, acompanham e entregam o trabalho. Cada projeto reúne metas, tarefas e marcos relacionados e permite acompanhar o progresso em um só lugar. <br /><br />
                    Seja para entregas da empresa ou iniciativas internas, os projetos dão a estrutura e as ferramentas para transformar ideias em resultados.
                </p><br />
            </div>
            <br /><br />
            <div class="row">
                <div class="col-md-12 tw-text-center">
                    <x-global::forms.button tag="a" link="javascript:void(0)" contentRole="tertiary" onclick="leantime.helperController.closeModal()">Vou explorar sozinho</x-global::forms.button>
                    <x-global::forms.button tag="a" link="javascript:void(0)" contentRole="primary" onclick="leantime.helperController.closeModal(); leantime.helperController.startProjectDashboardTour();">{{ __("buttons.start_tour") }} <i class="fa-solid fa-arrow-right"></i></x-global::forms.button>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-md-12 tw-text-center">
                    <form hx-post="{{ BASE_URL }}/help/helperModal/dontShowAgain" hx-trigger="change" hx-swap="none">
                        <label class="tw-text-sm tw-mt-sm" >
                            <input type="hidden" name="modalId" value="projectDashboard" />
                            <input type="checkbox" id="dontShowAgain" name="hidePermanently"  style="margin-top:-2px;">
                            Não mostrar novamente
                        </label>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

