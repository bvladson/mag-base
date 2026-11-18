<!DOCTYPE html>
<html dir="{{ __('language.direction') }}" lang="{{ __('language.code') }}">
<head>
    @include('global::sections.header')
    @stack('styles')
</head>

<body class="loginpage" style="height:100%;" hx-headers='{"X-CSRF-TOKEN": "{{ csrf_token() }}"}'>

<div class="header hidden-gt-sm tw-p-[10px]" style="background:var(--header-gradient)">
    <a href="{!! BASE_URL !!}">
        <img src="{{ BASE_URL }}/dist/images/mag/logo-cabecalho.svg" class="tw-h-full" alt="MAG"/>
    </a>
</div>

<div class="row" style="min-height:100vh; max-width: 98vw; height: auto;">
    <div class="col-md-4 hidden-phone regLeft">

        <div class="logo">
            <a href="{!! BASE_URL !!}">
                <img src="{{ BASE_URL }}/dist/images/mag/logo-login.svg" alt="Grupo MAG Móveis Corporativos" style="width:170px; max-width:100%; height:auto;" />
            </a>
        </div>

        <div class="welcomeContent">
            @dispatchFilter('welcomeText', '<h1 class="mainWelcome">'.$language->__("headlines.welcome_back").'</h1>')
        </div>

        @dispatchFilter('belowWelcomeText', '')

    </div>
    <div class="col-md-8 col-sm-12 regRight">

        <div class="regpanel">
            <div class="regpanelinner">

                @if($logoPath != '')
                    <a href="{!! BASE_URL !!}" target="_blank">

                        @if(!str_ends_with($logoPath, "dist/images/logo.svg" ))
                            <img src="{{ $logoPath }}" class="tw-h-full "/>
                        @endif
                    </a>
                @endif

                @isset($action, $module)
                    @include("$module::$action")
                @else
                    @yield('content')
                @endisset
            </div>
        </div>

    </div>
</div>

@include('global::sections.pageBottom')
@stack('scripts')
</body>

</html>
