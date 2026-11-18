<?php

namespace Leantime\Domain\Plugins\Hxcontrollers;

use Leantime\Core\Controller\HtmxController;

/**
 * MAG: removido da base — instalação de apps da loja do Leantime.
 *
 * A classe continua existindo porque o classmap otimizado do Composer a referencia
 * (apagar o arquivo faria a rota responder 500). Sem métodos get/post/run, o
 * Frontcontroller não encontra método válido e qualquer acesso responde 404.
 */
class Details extends HtmxController
{
    protected static string $view = 'plugins::plugindetails';
}
