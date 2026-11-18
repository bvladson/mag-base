@extends($layout)

@section('content')

    <x-auth::onboardingProgress :percentComplete="100" current="" :completed="['account', 'theme', 'personalization', 'time']" />

<h2>🎉 Tudo pronto para começar</h2>

<div class="regcontent">

    <form id="resetPassword" action="" method="post">

        <input type="hidden" name="step" value="5"/>
        <input type="hidden" name="complete" value="1"/>

        {{  $tpl->displayInlineNotification() }}

        <div class="row">
            <div class="col-md-6">
                <div class="ticketBox tw-p-[20px]">
                    <span class="fancyLink">Você sabia?</span><br />
                    <span style="font-size:16px;">Definir intenções comprovadamente <strong>mais que dobra a taxa de sucesso</strong> na conclusão de tarefas.</span>
                </div>
            </div>
            <div class="col-md-6">
                <x-global::undrawSvg image="undraw_adventure_map_hnin.svg" maxWidth="60%" maxHeight="300px"></x-global::undrawSvg>
            </div>
        </div>

        <p><br />A partir daqui, vamos ajudar você a transformar sua lista de tarefas em um projeto com metas. Depois, vamos trabalhar<br /> juntos para identificar suas tarefas mais importantes e criar algumas intenções<br />para fazer o trabalho acontecer.</p> <br />

        <br />
        <x-global::forms.button tag="input" inputType="submit" contentRole="primary" labelText="Concluir cadastro" name="createAccount" />


    </form>

</div>

@endsection
