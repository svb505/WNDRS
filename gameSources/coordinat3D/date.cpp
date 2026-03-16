#include "date.h"
#include <QDateTime>
#include <QString>

QDateTime getCurrentDate() { return QDateTime::currentDateTime(); }
QString getConvertedDate(const QDateTime& dateTime) { return dateTime.toString("dd.MM.yy"); }


