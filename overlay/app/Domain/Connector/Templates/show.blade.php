@extends($layout)

@section('content')

<div class="pageheader">
    <div class="pageicon"><i class="fa-solid fa-circle-nodes"></i></div>
    <div class="pagetitle">
       <h1>Integrações</h1>
    </div>
</div>

<div class="maincontent">
    <div class="maincontentinner">

        {!! $tpl->displayNotification() !!}
        <h5 class="subtitle">Sincronize o sistema com suas aplicações externas</h5>
        <p>Integrações disponíveis</p>

        <div class="row">
            @foreach ($providers as $provider)
                <div class="col-md-3">
                    <div class="profileBox">
                        <div class="commentImage gradient">
                            <img src="{{ BASE_URL }}/{{ $provider->image }}"/>
                        </div>
                        <span class="userName">
                            <strong>{{ $provider->name }}</strong>
                            <br /><small>Métodos disponíveis: {{ implode(', ', $provider->methods) }}</small>
                            <br /><br />
                            {!! $provider->description !!}
                        </span>
                        <br />

                        @if (isset($provider->button))
                            <x-global::forms.button tag="a" link="{{ $provider->button['url'] }}" contentRole="primary">{{ $provider->button['text'] }}</x-global::forms.button>
                        @else
                            <x-global::forms.button tag="a" link="{{ BASE_URL }}/connector/integration?provider={{ $provider->id }}" contentRole="primary">Criar integração</x-global::forms.button>
                        @endif

                        <div class="clearall"></div>
                    </div>
                </div>
            @endforeach
        </div>

    </div>

    {{-- Existing Integrations section placeholder --}}

</div>

@once
@push('scripts')
<script type="text/javascript">
   jQuery(document).ready(function() {
   });
</script>
@endpush
@endonce

@endsection
