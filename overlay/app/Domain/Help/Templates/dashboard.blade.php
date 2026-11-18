<div class="center padding-lg" style="width:800px;">
    <div class="row">
        <div class="col-md-12">
            <x-global::undrawSvg image="undraw_social_serenity_vhix.svg" maxWidth="auto"  maxheight="auto" height="250px" headline="{{ __('headlines.welcome') }}"></x-global::undrawSvg>
        </div>
    </div>
    <div class="row onboarding">
        <div class="col-md-12" style="font-size:var(--font-size-l);">
            <br />
            O sistema foi feito para ajudar você a enxergar o progresso rumo às suas metas.<br />
            <br />
            Estamos acostumados a criar listas de tarefas, mas aqui a proposta é pensar primeiro no que exatamente você quer alcançar.<br />
            <br />
            1. Defina uma visão (estratégia) e suas metas<br />
            2. Defina o trabalho que leva até essas metas<br />
            3. Alcance as metas, planejando o dia a dia no painel Meu Trabalho.<br />
            <br /><br />
            <x-global::forms.button tag="a" link="javascript:void(0)" contentRole="primary" onclick="leantime.helperController.hideAndKeepHidden('dashboard'); leantime.helperController.startProjectDashboardTour();">{{ __("buttons.lets_go") }} <i class="fa-solid fa-arrow-right"></i></x-global::forms.button>
            <div class="clearall"></div>
        </div>
    </div>
</div>
