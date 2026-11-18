@extends($layout)

@section('content')

@php
    $providerEntities = $providerEntities ?? [];
    $provider = $provider ?? null;
    $leantimeEntities = $leantimeEntities ?? [];
    $integrationId = $integrationId ?? null;

    $urlAppend = '';
    if (isset($integrationId) && is_numeric($integrationId)) {
        $urlAppend = '&integrationId=' . $integrationId;
    }
@endphp

<div class="pageheader">
    <div class="pageicon"><i class="fa-solid fa-circle-nodes"></i></div>
    <div class="pagetitle">
        <div class="row">
            <div class="col-lg-8">
                <h1>{!! __('headlines.connector') !!} // {{ $provider->name }}</h1>
            </div>
        </div>
    </div>
</div>

    <div class="maincontent">
        <div class="maincontentinner">
            @include('connector::submodules.importProgress')
        </div>
        <div class="maincontentinner center">

        {!! $tpl->displayNotification() !!}

            <h5 class="subtitle">O que você está importando?</h5>
            <br />
            Nesta tela você escolhe o que deseja sincronizar. Selecione uma entidade à esquerda e associe-a a um item do sistema à direita.
            The arrow indicates that we will synchronize from one location to the other.<br /><br />

            <form method="post" action="{{ BASE_URL }}/connector/integration/?provider={{ $provider->id }}&step=fields{{ $urlAppend }}">

                <div class="row">
                    <div class="col-md-3"></div>
                    <div class="col-md-2 right">
                        <h1>De (sua integração)</h1>
                        <label for="providerEntities">{{ $provider->name }}</label>
                        <select name="providerEntities" id="providerEntities" style="width:100%;">
                            @foreach ($providerEntities as $key => $entity)
                                <option value="{{ $key }}">{{ $entity['name'] }}</option>
                            @endforeach
                        </select>
                    </div>
                    <div class="col-md-2" style="padding-top:50px;">
                        <i class="fa fa-arrow-right"></i>
                    </div>
                    <div class="col-md-2">
                        <h1>Para (MAG)</h1>

                        <label for="leantimeEntities">MAG</label>
                        <select name="leantimeEntities" id="leantimeEntities" style="width:100%;">
                            @foreach ($leantimeEntities as $key => $entity)
                                <option value="{{ $key }}">{{ $entity['name'] }}</option>
                            @endforeach
                        </select>
                    </div>
                    <div class="col-md-3"></div>
                </div>

                <div class="left">
                    <x-global::forms.button tag="a" link="{{ BASE_URL }}/connector/integration/?provider={{ $provider->id }}" contentRole="tertiary" class="pull-left">Voltar</x-global::forms.button>
                </div>

                <div class="right">
                    <x-global::forms.button tag="input" inputType="submit" labelText="Next" />
                </div>
                <div class="clearall"></div>
            </form>
        </div>
    </div>

@endsection
