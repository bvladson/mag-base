@extends($layout)

@section('content')

<x-auth::onboardingProgress :percentComplete="64" current="personalization" :completed="['account', 'theme']" />

<h2>🎨 Deixando a visualização confortável</h2>
<p>Seu modo e esquema de cores preferidos.<br /></p>

<div class="regcontent">

    <form id="resetPassword" action="" method="post">
        <input type="hidden" name="step" value="3" />

        {{  $tpl->displayInlineNotification() }}



        <div class="row">
            <div class="col-md-12">
                <label for="colormode" >{{ __('label.colormode') }}</label>

                <x-global::selectable :selected="($userColorMode == 'light') ? 'true' : ''" :id="'light'" :name="'colormode'" :value="'light'" :label="'Claro'" onclick="jQuery('#themeStyleSheetDark').remove(); leantime.snippets.toggleTheme('light')">
                    <label for="colormode-light" class="tw-w-[200px]">
                        <i class="fa-solid fa-sun tw-font-xxl"></i>
                    </label>
                </x-global::selectable>

                <x-global::selectable :selected="($userColorMode == 'dark') ? 'true' : ''" :id="'dark'" :name="'colormode'" :value="'dark'" :label="'Escuro'" onclick="jQuery('#themeStyleSheetDark').remove(); leantime.snippets.toggleTheme('dark')">
                    <label for="colormode-light" class="tw-w-[200px]">
                        <i class="fa-solid fa-moon tw-font-xxl"></i>
                    </label>
                </x-global::selectable>

                {{-- MAG: seguir o modo claro/escuro do sistema operacional --}}
                <x-global::selectable :selected="($userColorMode == 'system') ? 'true' : ''" :id="'system'" :name="'colormode'" :value="'system'" :label="'Sistema'" onclick="leantime.snippets.toggleTheme(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')">
                    <label for="colormode-system" class="tw-w-[200px]">
                        <i class="fa-solid fa-desktop tw-font-xxl"></i>
                    </label>
                </x-global::selectable>
            </div>
        </div>
        <br />
        <div class="row">
            <div class="col-md-12">
                <label>Esquema de cores</label>
                @foreach($availableColorSchemes as $key => $scheme )
                    <x-global::selectable class="circle" :selected="($userColorScheme == $key) ? 'true' : ''" :id="$key" :name="'colorscheme'" :value="$key" :label="__($scheme['name'])"  onclick="leantime.snippets.toggleColors('{{ $scheme['primaryColor'] }}','{{ $scheme['secondaryColor'] }}');">
                        <label for="color-{{ $key }}" class="colorCircle"
                               style="background:linear-gradient(135deg, {{ $scheme["primaryColor"] }} 20%, {{ $scheme["secondaryColor"] }} 100%);">
                        </label>
                    </x-global::selectable>
                @endforeach

            </div>
        </div>
        <br /> <br />
        <div class="tw-text-right">
            <x-global::forms.button tag="a" link="{{BASE_URL}}/auth/userInvite/{{$inviteId}}?step=2" contentRole="tertiary" style="width:auto; margin-right:10px">Voltar</x-global::forms.button>
            <input type="submit" name="createAccount" class="tw-w-auto" style="width:auto" value="<?php echo $tpl->language->__("buttons.next"); ?>" />
        </div>


    </form>

</div>

@endsection
