<?php

namespace Leantime\Domain\Plugins\Controllers;

use Leantime\Core\Controller\Controller;

/**
 * MAG: removido da base — loja de apps do Leantime (marketplace.leantime.io).
 *
 * A classe continua existindo porque o classmap otimizado do Composer a referencia
 * (apagar o arquivo faria a rota responder 500). Sem métodos get/post/run, o
 * Frontcontroller não encontra método válido e qualquer acesso responde 404.
 */
class Marketplace extends Controller
{
}
